from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm

from users.models import User


class StyleFormMixin:
    """
   Обновление стилей форм восстановления пароля
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control mt-2',
                'autocomplete': 'off'
            })


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма авторизации на сайте
    """
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации на сайте
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля
    """
    pass


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """
    pass


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
     Форма обновления данных пользователя
     """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
