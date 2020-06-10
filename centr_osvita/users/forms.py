from django.core.validators import MinLengthValidator
from django.forms import ModelForm, CharField, PasswordInput

from centr_osvita.users.models import User


class UserRegisterForm(ModelForm):
    password = CharField(widget=PasswordInput, validators=[MinLengthValidator(limit_value=8)])

    class Meta:
        model = User
        fields = ['phone', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.phone
        user.set_password(user.password)
        user.email = user.phone.as_e164+'@dumpy.com'  # create dumpy email
        if commit:
            user.save()
        return user
