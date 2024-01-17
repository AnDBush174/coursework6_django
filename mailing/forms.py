from django import forms

from mailing.models import MailingMessage, MailingSettings


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
    class Meta:
        model = MailingMessage
        exclude = ('owner',)


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ('is_published',)

