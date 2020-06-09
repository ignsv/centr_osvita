from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.http import Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect

from centr_osvita.quiz.forms import CommonAnswerForm, OrderAnswerForm, MappingAnswerForm
from centr_osvita.quiz.mixins import IsStaffRequiredMixin
from centr_osvita.quiz.models import Quiz, Subject, Question, QUESTION_TYPES


class QuizResultView(IsStaffRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/results.html'
    queryset = Quiz.objects.filter(status__in=(Quiz.QUIZ_STATUS_TYPES.suspend, Quiz.QUIZ_STATUS_TYPES.done))


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'quiz/subject_list.html'

    def get_queryset(self):
        param = self.request.GET.get('q')
        object_list = Subject.objects.all()
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
        self.instance = Subject.objects.filter(pk=pk).first()
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
            return redirect('common:home')

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
            pass
        context['form'] = form
        context['object'] = self.instance
        context['question'] = self.current_question

        return render(request, self.template_name, context)
