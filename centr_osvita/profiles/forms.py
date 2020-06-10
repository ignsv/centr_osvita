from django.forms import ModelForm, ValidationError
from centr_osvita.profiles.models import Profile
from django.utils.translation import ugettext_lazy as _


class ProfileRegisterForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'mother_full_name', 'mother_phone', 'father_full_name', 'father_phone', 'school_name']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user', None)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data['mother_full_name'] or cleaned_data['father_full_name']):
            raise ValidationError(_("You should enter at least one parent name"))
        if 'mother_phone' in cleaned_data and 'father_phone' in cleaned_data:
            if cleaned_data['mother_full_name'] and not cleaned_data['mother_phone'] \
                    or cleaned_data['father_full_name'] and not cleaned_data['father_phone']:
                raise ValidationError(_("You should enter full parent credentials"))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()
        return instance
