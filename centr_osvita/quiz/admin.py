from django.contrib import admin

from centr_osvita.quiz.models import Subject, Test, Question, CommonAnswer, OrderAnswer, MappingAnswer, Answer, Quiz, \
    QuizCommonAnswer, QuizOrderAnswer, QuizMappingAnswer, QuizAnswer, QuizQuestion, Year, YearSubjectStatistics, \
    TestParameter
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('date', )


@admin.register(YearSubjectStatistics)
class YearSubjectStatisticsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')


@admin.register(TestParameter)
class TestParamAdmin(admin.ModelAdmin):
    list_display = ('id',)


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
    inlines = (AnswerInline,)
    search_fields = ('test__name', 'text')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('test', 'status', 'student')
    search_fields = ('test__name', 'student__full_name')
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
