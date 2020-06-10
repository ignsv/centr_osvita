from django import forms
from django.utils.translation import ugettext as _

from centr_osvita.quiz.models import CommonAnswer, OrderAnswer, MappingAnswer


class CommonAnswerForm(forms.Form):
    number = forms.ChoiceField(choices=CommonAnswer.ORDER_COMMON, widget=forms.RadioSelect(),
                               initial=CommonAnswer.ORDER_COMMON.first)


class OrderAnswerForm(forms.Form):
    position_1 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                   initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())
    position_2 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                   initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())
    position_3 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                   initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())
    position_4 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                   initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super().clean()
        key_list = [int(cleaned_data['position_1']), int(cleaned_data['position_2']),
                    int(cleaned_data['position_3']), int(cleaned_data['position_4'])]
        if len(set(key_list)) != 4:
            raise forms.ValidationError(_("You should enter different values"))


class MappingAnswerForm(forms.Form):
    position_1 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                   initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
    position_2 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                   initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
    position_3 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                   initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
    position_4 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                   initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super().clean()
        key_list = [int(cleaned_data['position_1']), int(cleaned_data['position_2']),
                    int(cleaned_data['position_3']), int(cleaned_data['position_4'])]
        if len(set(key_list)) != 4:
            raise forms.ValidationError(_("You should enter different values"))