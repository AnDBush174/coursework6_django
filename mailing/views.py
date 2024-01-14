from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm
from mailing.models import MailingMessage, MailingSettings


class MailingListView(ListView):
    paginate_by = 50
    model = MailingMessage
    template_name = 'mailing/mailing_list.html'
    extra_context = {'title': 'Список рассылок'}


class MailingDetailView(DetailView):
    model = MailingMessage
    template_name = 'mailing/mailing_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs.get('pk'))
        context['settings'] = MailingSettings.objects.filter(message_id=self.kwargs.get('pk'))
        print(context['settings'])
        return context


class MailingCreateView(CreateView):
    model = MailingMessage
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        VersionFormset = inlineformset_factory(MailingMessage, MailingSettings, form=MailingForm,
                                               can_delete=False, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST)
        else:
            context['formset'] = VersionFormset()
        return context

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #     formset = self.get_context_data()['formset']
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)

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

    # def get_success_url(self):
    #     return reverse('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = MailingMessage
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        VersionFormset = inlineformset_factory(MailingMessage, MailingSettings, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
                return super().form_valid(form)
            else:
                return self.form_invalid(form)

    # def form_valid(self, form):
    #     formset = self.get_context_data().get('formset')
    #     if self.request.user == self.object.owner or self.request.user.is_superuser:
    #         formset.save()
    #         return super().form_valid(form)
    #     return self.form_invalid(form)


class MailingDeleteView(DeleteView):
    model = MailingMessage
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

