from django.core.validators import MinLengthValidator
from django.forms import ModelForm, CharField, PasswordInput

from centr_osvita.users.models import User


class UserRegisterForm(ModelForm):
    password = CharField(widget=PasswordInput, validators=[MinLengthValidator(limit_value=8)])

    class Meta:
        model = User
        fields = ['phone', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.phone
        user.set_password(user.password)
        user.email = user.phone.as_e164+'@dumpy.com'  # create dumpy email
        if commit:
            user.save()
        return user
