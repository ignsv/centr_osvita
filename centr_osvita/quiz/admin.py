from django.contrib import admin

from centr_osvita.quiz.models import Subject, Question, CommonAnswer, OrderAnswer, MappingAnswer, Answer
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')


class AnswerInline(StackedPolymorphicInline):
    class CommonAnswerInline(StackedPolymorphicInline.Child):
        model = CommonAnswer

    class OrderAnswerInline(StackedPolymorphicInline.Child):
        model = OrderAnswer

    class MappingAnswerInline(StackedPolymorphicInline.Child):
        model = MappingAnswer

    model = Answer
    child_inlines = (
        CommonAnswerInline,
        OrderAnswerInline,
        MappingAnswerInline,
    )


@admin.register(Question)
class QuestionAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    list_display = ('type',)
    inlines = (AnswerInline,)
    search_fields = ('subject__name', 'text')
