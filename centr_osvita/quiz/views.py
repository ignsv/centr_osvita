from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from centr_osvita.quiz.mixins import IsStaffRequiredMixin
from centr_osvita.quiz.models import Quiz, Subject


class QuizResultView(IsStaffRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/results.html'
    queryset = Quiz.objects.filter(status__in=(Quiz.QUIZ_STATUS_TYPES.suspend, Quiz.QUIZ_STATUS_TYPES.done))


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'quiz/subject_list.html'

    def get_queryset(self): # new
        param = self.request.GET.get('q')
        object_list = Subject.objects.all()
        if param:
            object_list = object_list.filter(name__search=param)
        return object_list


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'quiz/subject_detail.html'
