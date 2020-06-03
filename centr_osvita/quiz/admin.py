from django.contrib import admin

from centr_osvita.quiz.models import Subject, Question, CommonAnswer, OrderAnswer, MappingAnswer, Answer, Quiz, \
    QuizCommonAnswer, QuizOrderAnswer, QuizMappingAnswer, QuizAnswer, QuizQuestion
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


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'student')
    search_fields = ('subject__name', 'student__full_name')
    list_filter = ('status',)


class QuizAnswerInline(StackedPolymorphicInline):
    class QuizCommonAnswerInline(StackedPolymorphicInline.Child):
        model = QuizCommonAnswer

    class QuizOrderAnswerInline(StackedPolymorphicInline.Child):
        model = QuizOrderAnswer

    class QuizMappingAnswerInline(StackedPolymorphicInline.Child):
        model = QuizMappingAnswer

    model = QuizAnswer
    child_inlines = (
        QuizCommonAnswerInline,
        QuizOrderAnswerInline,
        QuizMappingAnswerInline,
    )


@admin.register(QuizQuestion)
class QuizQuestionAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = (QuizAnswerInline,)
    search_fields = ('question__id',)
