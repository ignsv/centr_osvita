from .views import TestView, TestListView, QuizResultView, FinishQuizView, CancelTestView
from django.conf.urls import url

urlpatterns = [
    url(r'^results/(?P<pk>\d+)$', QuizResultView.as_view(), name='admin-quiz-result'),
    url(r'^list/$', TestListView.as_view(), name='test-list'),
    url(r'^finish/(?P<pk>\d+)$', FinishQuizView.as_view(), name='quiz-finish'),
    url(r'^cancel/(?P<pk>\d+)$', CancelTestView.as_view(), name='quiz-cancel'),
    url(r'^(?P<pk>\d+)$', TestView.as_view(), name='test-detail'),
]
