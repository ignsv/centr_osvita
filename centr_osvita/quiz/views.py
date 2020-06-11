from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.http import Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect

from centr_osvita.quiz.forms import CommonAnswerForm, OrderAnswerForm, MappingAnswerForm
from centr_osvita.quiz.mixins import IsStaffRequiredMixin
from centr_osvita.quiz.models import Quiz, Subject, Question, QUESTION_TYPES, QuizCommonAnswer, \
    QuizOrderAnswer, OrderAnswer, QuizMappingAnswer, MappingAnswer, QuizQuestion, CommonAnswer


class QuizResultView(IsStaffRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/results.html'
    queryset = Quiz.objects.filter(status__in=(Quiz.QUIZ_STATUS_TYPES.suspend, Quiz.QUIZ_STATUS_TYPES.done))


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'quiz/subject_list.html'

    def get_queryset(self):
        param = self.request.GET.get('q')
        object_list = Subject.objects.filter(status=True)
        if param:
            object_list = object_list.filter(name__search=param)
        return object_list


class SubjectView(LoginRequiredMixin, View):
    template_name = 'quiz/subject_detail.html'
    current_question = None
    current_quiz = None
    instance = None
    current_form = None

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.instance = Subject.objects.filter(pk=pk, status=True).first()
        if not self.instance:
            raise Http404(_("Not found"))
        if not Quiz.objects.filter(student=request.user.profile, status=Quiz.QUIZ_STATUS_TYPES.progress).count():
            Quiz.objects.create(subject=self.instance, student=request.user.profile)

        self.current_quiz = Quiz.objects.filter(student=self.request.user.profile,
                                                status=Quiz.QUIZ_STATUS_TYPES.progress).first()
        used_question_ids = self.current_quiz.quiz_questions.values_list('question__id', flat=True)

        self.current_question = Question.objects.filter(subject=self.instance, type=QUESTION_TYPES.common).exclude(
            id__in=used_question_ids).first()
        if not self.current_question:
            self.current_question = Question.objects.filter(subject=self.instance, type=QUESTION_TYPES.order).exclude(
                id__in=used_question_ids).first()
        if not self.current_question:
            self.current_question = Question.objects.filter(subject=self.instance, type=QUESTION_TYPES.mapping).exclude(
                id__in=used_question_ids).first()

        self.current_form = None
        if self.current_question is not None:
            if self.current_question.type == QUESTION_TYPES.common:
                self.current_form = CommonAnswerForm()
            elif self.current_question.type == QUESTION_TYPES.order:
                self.current_form = OrderAnswerForm()
            else:
                self.current_form = MappingAnswerForm()

        if not self.current_question:
            self.current_quiz.status = Quiz.QUIZ_STATUS_TYPES.done
            self.current_quiz.save()
            return redirect('quiz:quiz-finish')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = dict()
        context['object'] = self.instance
        context['question'] = self.current_question
        context['form'] = self.current_form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = dict()
        form = None
        if self.current_question is not None:
            if self.current_question.type == QUESTION_TYPES.common:
                form = CommonAnswerForm(request.POST)
            elif self.current_question.type == QUESTION_TYPES.order:
                form = OrderAnswerForm(request.POST)
            else:
                form = MappingAnswerForm(request.POST)

        if form.is_valid():
            quiz_question = QuizQuestion.objects.create(quiz=self.current_quiz, question=self.current_question,
                                                        status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.done)
            answers_ids = self.current_question.answer_set.values_list('id', flat=True)
            if self.current_question.type == QUESTION_TYPES.common:
                answer = CommonAnswer.objects.filter(id__in=answers_ids, number=form.cleaned_data['number']).first()
                QuizCommonAnswer.objects.create(quiz_question=quiz_question, number=form.cleaned_data['number'],
                                                answer=answer)
            elif self.current_question.type == QUESTION_TYPES.order:
                answer_1 = OrderAnswer.objects.filter(id__in=answers_ids,
                                                      number_1=OrderAnswer.ORDER_FIRST_CHAIN.first).first()
                QuizOrderAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_1'],
                                               number_1=answer_1.number_1, answer=answer_1)
                answer_2 = OrderAnswer.objects.filter(id__in=answers_ids,
                                                      number_1=OrderAnswer.ORDER_FIRST_CHAIN.second).first()
                QuizOrderAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_2'],
                                               number_1=answer_2.number_1, answer=answer_2)
                answer_3 = OrderAnswer.objects.filter(id__in=answers_ids,
                                                      number_1=OrderAnswer.ORDER_FIRST_CHAIN.third).first()
                QuizOrderAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_3'],
                                               number_1=answer_3.number_1, answer=answer_3)
                answer_4 = OrderAnswer.objects.filter(id__in=answers_ids,
                                                      number_1=OrderAnswer.ORDER_FIRST_CHAIN.fourth).first()
                QuizOrderAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_4'],
                                               number_1=answer_4.number_1, answer=answer_4)
            else:
                key_list = [int(form.cleaned_data['position_1']), int(form.cleaned_data['position_2']),
                            int(form.cleaned_data['position_3']), int(form.cleaned_data['position_4'])]
                answer_1 = MappingAnswer.objects.filter(id__in=answers_ids,
                                                        number_1=MappingAnswer.FIRST_CHAIN_TYPES.first).first()
                QuizMappingAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_1'],
                                                 number_1=answer_1.number_1, answer=answer_1)
                answer_2 = MappingAnswer.objects.filter(id__in=answers_ids,
                                                        number_1=MappingAnswer.FIRST_CHAIN_TYPES.second).first()
                QuizMappingAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_2'],
                                                 number_1=answer_2.number_1, answer=answer_2)
                answer_3 = MappingAnswer.objects.filter(id__in=answers_ids,
                                                        number_1=MappingAnswer.FIRST_CHAIN_TYPES.third).first()
                QuizMappingAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_3'],
                                                 number_1=answer_3.number_1, answer=answer_3)
                answer_4 = MappingAnswer.objects.filter(id__in=answers_ids,
                                                        number_1=MappingAnswer.FIRST_CHAIN_TYPES.fourth).first()
                QuizMappingAnswer.objects.create(quiz_question=quiz_question, number_2=form.cleaned_data['position_4'],
                                                 number_1=answer_4.number_1, answer=answer_4)
                answer_5 = MappingAnswer.objects.filter(id__in=answers_ids,
                                                        number_1=MappingAnswer.FIRST_CHAIN_TYPES.zero).first()
                second_order_list = []
                for key, value in MappingAnswer.SECOND_CHAIN_TYPES:
                    second_order_list.append(key)
                second_key = [x for x in second_order_list if x not in key_list][0]

                QuizMappingAnswer.objects.create(quiz_question=quiz_question, number_2=second_key,
                                                 number_1=answer_5.number_1, answer=answer_5)

            return redirect('quiz:subject-detail', self.instance.id)
        else:
            context['form'] = form
            context['object'] = self.instance
            context['question'] = self.current_question
            return render(request, self.template_name, context)


class EndQuizView(LoginRequiredMixin, View):
    model = Subject
    template_name = 'quiz/test_ending.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
