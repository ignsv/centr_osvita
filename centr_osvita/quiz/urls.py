from .views import TestView, TestListView, QuizResultView, EndQuizView
from django.conf.urls import url

urlpatterns = [
    url(r'^results/(?P<pk>\d+)$', QuizResultView.as_view(), name='quiz-result'),
    url(r'^list/$', TestListView.as_view(), name='test-list'),
    url(r'^finish/$', EndQuizView.as_view(), name='quiz-finish'),
    url(r'^(?P<pk>\d+)$', TestView.as_view(), name='test-detail'),
]
