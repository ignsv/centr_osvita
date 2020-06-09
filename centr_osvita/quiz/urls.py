from .views import SubjectView, SubjectListView, QuizResultView
from django.conf.urls import url

urlpatterns = [
    url(r'^results/(?P<pk>\d+)$', QuizResultView.as_view(), name='quiz-result'),
    url(r'^list/$', SubjectListView.as_view(), name='subject-list'),
    url(r'^(?P<pk>\d+)$', SubjectView.as_view(), name='subject-detail'),
]
