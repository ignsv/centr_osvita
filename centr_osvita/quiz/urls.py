from .views import QuizDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^results/(?P<pk>\d+)$', QuizDetailView.as_view(), name='quiz-detail'),
]
