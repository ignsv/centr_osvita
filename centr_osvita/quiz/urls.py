from .views import TestView, TestListView, QuizResultView, FinishQuizView, CancelTestView, ProfileReportsView
from django.conf.urls import url

urlpatterns = [
    url(r'^results/(?P<pk>\d+)$', QuizResultView.as_view(), name='admin-quiz-result'),
    url(r'^reports/(?P<pk>\d+)$', ProfileReportsView.as_view(), name='admin-profile-report'),
    url(r'^list/$', TestListView.as_view(), name='test-list'),
    url(r'^finish/(?P<pk>\d+)$', FinishQuizView.as_view(), name='quiz-finish'),
    url(r'^cancel/(?P<pk>\d+)$', CancelTestView.as_view(), name='quiz-cancel'),
    url(r'^(?P<pk>\d+)$', TestView.as_view(), name='test-detail'),
]
