from django import forms
from django.forms import ModelForm
from centr_osvita.profiles.models import Profile


class ProfileRegisterForm(ModelForm):
    grade = forms.ChoiceField(choices=Profile.GRADE_NUMBER, initial=Profile.GRADE_NUMBER.nine, required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'parent_full_name', 'parent_phone', 'institution_name', 'grade']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user', None)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.grade:
            instance.grade = None
        instance.user = self.user

        if commit:
            instance.save()
        return instance
