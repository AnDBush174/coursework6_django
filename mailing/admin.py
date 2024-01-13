# from django.contrib import admin
# from .models import Mailing, MailingMessage
#
#
# class MailingMessageInline(admin.StackedInline):
#     model = MailingMessage
#     max_num = 1
#     min_num = 1
#     can_delete = False
#     verbose_name = 'сообщение рассылки'
#     verbose_name_plural = 'сообщения рассылки'
#
#
# @admin.register(Mailing)
# class MailingAdmin(admin.ModelAdmin):
#     list_display = ('mailing_start', 'mailing_end', 'mailing_period', 'mailing_status',)
#     list_filter = ('mailing_start', 'mailing_end', 'mailing_period', 'mailing_status',)
#     filter_horizontal = ('recipient',)
#     inlines = [
#         MailingMessageInline,
#     ]
