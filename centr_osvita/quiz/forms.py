from django import forms
from django.forms import BaseFormSet
from django.utils.translation import ugettext as _

from centr_osvita.quiz.models import CommonAnswer, OrderAnswer, MappingAnswer


class AnswerValidatedFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        key_list = [form.cleaned_data['position'] for form in self.forms]
        if len(set(key_list)) != len(self.forms):
            raise forms.ValidationError(_('You should enter different values'))


class AnswerForm(forms.Form):
    position = forms.ChoiceField(choices=CommonAnswer.ORDER_COMMON, widget=forms.RadioSelect(),
                                 initial=CommonAnswer.ORDER_COMMON.first)


class OrderAnswerForm(forms.Form):
    position = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                 initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())

