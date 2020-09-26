from django.apps import AppConfig


class QuizConfig(AppConfig):
    name = 'centr_osvita.quiz'

    def ready(self):
        from centr_osvita.quiz import signals
