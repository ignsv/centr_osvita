from django.views.generic.detail import DetailView

from centr_osvita.quiz.mixins import IsStaffRequiredMixin
from centr_osvita.quiz.models import Quiz


class QuizDetailView(IsStaffRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/results.html'
    queryset = Quiz.objects.filter(status__in=(Quiz.QUIZ_STATUS_TYPES.suspend, Quiz.QUIZ_STATUS_TYPES.done))
