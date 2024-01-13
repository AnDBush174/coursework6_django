from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published',)
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.add_article'


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published',)
    success_url = reverse_lazy('blog:view_article')
    permission_required = 'blog.change_article'

    def form_valid(self, form):
        instance = form.save(commit=True)
        instance.slug = slugify(instance.title)
        instance.save()
        return redirect(reverse('blog:view_article', args=[instance.slug]))


class ArticleListView(ListView):
    paginate_by = 10
    model = Article
    extra_context = {'title': 'Блог'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('-created_on')
        return queryset


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.delete_article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление "{self.object.title}"'
        return context
