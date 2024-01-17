from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, ManagerMailingForm
from mailing.models import MailingMessage, MailingSettings


class MailingListView(LoginRequiredMixin, ListView):
    paginate_by = 50
    model = MailingMessage
    template_name = 'mailing/mailing_list.html'
    extra_context = {'title': 'Список рассылок'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.view_mailingmessage'):
            return queryset.order_by('-is_published')
        else:
            return queryset.filter(owner=self.request.user).order_by('-setting__mailing_start')


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingMessage
    template_name = 'mailing/mailing_details.html'
    permission_required = 'mailing.view_mailingmessage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = MailingSettings.objects.filter(message_id=self.kwargs.get('pk'))
        return context

    def has_permission(self):
        obj = self.get_object()
        return obj.owner == self.request.user or super().has_permission()

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для просмотра этого объекта.")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылки'
        formset_factory = inlineformset_factory(MailingMessage, MailingSettings, form=MailingForm,
                                                can_delete=False, extra=1)
        if self.request.method == 'POST':
            context['formset'] = formset_factory(self.request.POST)
        else:
            context['formset'] = formset_factory()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

            formset.instance = self.object
            formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingMessage
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование рассылки'
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            formset_factory = inlineformset_factory(MailingMessage, MailingSettings, form=MailingForm, extra=1)
            if self.request.method == 'POST':
                context['formset'] = formset_factory(self.request.POST, instance=self.object)
            else:
                context['formset'] = formset_factory(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data().get('formset')
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            if formset.is_valid():
                formset.save()
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return (obj.owner == self.request.user
                or self.request.user.has_perms(['mailing.can_cancel_mailing'])
                or self.request.user.is_superuser)

    def get_form_class(self):
        if not self.request.user.is_superuser and self.request.user.has_perm('mailing.can_cancel_mailing'):
            return ManagerMailingForm
        return MailingForm

    def form_invalid(self, form):
        pass


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.owner == self.request.user
