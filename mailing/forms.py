from django import forms

from clients.models import Client
from mailing.models import MailingMessage, MailingSettings
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control mt-2 mb-2'


class MailingForm(StyleFormMixin, forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(queryset=Client.objects.none(), widget=forms.SelectMultiple)

    class Meta:
        model = MailingMessage
        fields = ['subject', 'body', 'recipients', 'is_published']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user and isinstance(user, User):
            if user.is_superuser:
                self.fields['recipients'].queryset = Client.objects.all()
            else:
                self.fields['recipients'].queryset = Client.objects.filter(owner=user)

    def save(self, commit=True):
        mailing_message = super().save()
        if commit:
            mailing_message.recipient.set(self.cleaned_data['recipients'])
        return mailing_message


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = '__all__'


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ('is_published',)

    def __init__(self, *args, **kwargs):
        kwargs.pop('user')
        super().__init__(*args, **kwargs)

