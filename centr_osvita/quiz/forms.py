from django import forms

from centr_osvita.quiz.models import CommonAnswer, OrderAnswer, MappingAnswer


class CommonAnswerForm(forms.Form):
    number = forms.ChoiceField(choices=CommonAnswer.ORDER_COMMON, widget=forms.RadioSelect(),
                               initial=CommonAnswer.ORDER_COMMON.first)


class OrderAnswerForm(forms.Form):
    number_1 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                 initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())
    number_2 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                 initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())
    number_3 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                 initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())
    number_4 = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                 initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())


class MappingAnswerForm(forms.Form):
    number_1 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                 initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
    number_2 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                 initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
    number_3 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                 initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
    number_4 = forms.ChoiceField(choices=MappingAnswer.SECOND_CHAIN_TYPES,
                                 initial=MappingAnswer.SECOND_CHAIN_TYPES.first, widget=forms.RadioSelect())
