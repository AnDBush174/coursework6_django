from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from blog.models import Article
from clients.models import Client
from mailing.models import MailingSettings


class MainPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['total_mailings'] = MailingSettings.objects.count()
        context['total_active_mailings'] = (MailingSettings.objects.
                                            filter(mailing_status=MailingSettings.STATUS.RUNNING).count())
        context['total_unique_emails'] = Client.objects.values('email').annotate(total=Count('email')).count()
        context['blog'] = Article.objects.order_by('?')[:3]
        return context
