from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from model_utils.choices import Choices
import time

from centr_osvita.profiles.models import Profile

QUESTION_TYPES = Choices(
    (0, 'common', 'common'),
    (1, 'order', 'order'),
    (2, 'mapping', 'mapping'),
)


def question_image_path(instance, filename):
    dot_position = filename.find('.')
    return 'subject_{0}/{1}'.format(str(instance.subject.id),
                                    filename[:dot_position]+str(int(time.time()))+filename[dot_position:])


class Subject(TimeStampedModel):
    name = models.CharField(_('Subject name'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    status = models.BooleanField(_('Publish status'))

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return self.name


class Question(TimeStampedModel):
    subject = models.ForeignKey(Subject, verbose_name=_('Subject'), on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(_('Text'))
    image = models.ImageField(_("Image"), upload_to=question_image_path, null=True, blank=True)
    type = models.IntegerField(_("Question Type"), choices=QUESTION_TYPES, default=QUESTION_TYPES.common)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.text[:20]

    @property
    def ordered_answers_by_position(self):
        answers_ids = self.answer_set.values_list('id', flat=True)
        if self.type == QUESTION_TYPES.common:
            return CommonAnswer.objects.filter(id__in=answers_ids).order_by('number')
        elif self.type == QUESTION_TYPES.order:
            return OrderAnswer.objects.filter(id__in=answers_ids).order_by('number_1')
        if self.type == QUESTION_TYPES.mapping:
            return MappingAnswer.objects.filter(id__in=answers_ids).order_by('number_1')
        return self.answer_set


# Needs to correct deletion
# Workaround https://github.com/django-polymorphic/django-polymorphic/issues/229#issuecomment-398434412
def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class Answer(PolymorphicModel, TimeStampedModel):
    question = models.ForeignKey(Question, verbose_name=_('Question'), on_delete=NON_POLYMORPHIC_CASCADE)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    @property
    def type(self):
        return self._meta.object_name

    def __str__(self):
        return str(self.id)


class CommonAnswer(Answer):
    ORDER_COMMON = Choices(
        (1, 'first', 'A'),
        (2, 'second', 'B'),
        (3, 'third', 'C'),
        (4, 'fourth', 'D'),
    )
    text = models.CharField(_('Text'), max_length=255)
    number = models.IntegerField(_("Answer Order"), choices=ORDER_COMMON)
    correct = models.BooleanField(_('Correct answer'))

    class Meta:
        verbose_name = _('Common Answer')
        verbose_name_plural = _('Common Answers')

    def __str__(self):
        return '{}__{}:{}'.format(self.question.id, self.id, self.number)


class OrderAnswer(Answer):
    ORDER_FIRST_CHAIN = Choices(
        (1, 'first', '1'),
        (2, 'second', '2'),
        (3, 'third', '3'),
        (4, 'fourth', '4'),
    )
    ORDER_SECOND_CHAIN = Choices(
        (1, 'first', 'A'),
        (2, 'second', 'B'),
        (3, 'third', 'C'),
        (4, 'fourth', 'D'),
    )

    text = models.CharField(_('Text'), max_length=255)
    number_1 = models.IntegerField(_("Answer FIRST Position"), choices=ORDER_FIRST_CHAIN)
    number_2 = models.IntegerField(_("Answer SECOND Position"), choices=ORDER_SECOND_CHAIN)

    class Meta:
        verbose_name = _('Order Answer')
        verbose_name_plural = _('Order Answers')

    def __str__(self):
        return '{}__{}:{}_{}'.format(self.question.id, self.id, self.number_1, self.number_2)


class MappingAnswer(Answer):
    FIRST_CHAIN_TYPES = Choices(
        (1, 'first', '1'),
        (2, 'second', '2'),
        (3, 'third', '3'),
        (4, 'fourth', '4'),
        (0, 'zero', '0'),
    )
    SECOND_CHAIN_TYPES = Choices(
        (1, 'first', 'A'),
        (2, 'second', 'B'),
        (3, 'third', 'C'),
        (4, 'fourth', 'D'),
        (5, 'fifth', 'E'),
    )

    number_1 = models.IntegerField(_("First chain"), choices=FIRST_CHAIN_TYPES)
    number_2 = models.IntegerField(_("Second chain"), choices=SECOND_CHAIN_TYPES)
    text_1 = models.CharField(_('Text 1'), null=True, blank=True, max_length=255)
    text_2 = models.CharField(_('Text 2'), max_length=255)

    class Meta:
        verbose_name = _('Mapping Answer')
        verbose_name_plural = _('Mapping Answers')

    def __str__(self):
        return '{}__{}:{}_{}'.format(self.question.id, self.id, self.number_1, self.number_2)


class Quiz(TimeStampedModel):
    QUIZ_STATUS_TYPES = Choices(
        (0, 'progress', 'In Progress'),
        (1, 'done', 'Done'),
        (2, 'suspend', 'Suspend'),
    )
    subject = models.ForeignKey(Subject, verbose_name=_('Subject'), on_delete=models.CASCADE, related_name='quizzes')
    status = models.IntegerField(_("Status"), choices=QUIZ_STATUS_TYPES, default=QUIZ_STATUS_TYPES.progress)
    student = models.ForeignKey(Profile, verbose_name=_('Student'), on_delete=models.CASCADE, related_name='quizzes')

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    def __str__(self):
        return '{}_{}'.format(self.subject.name, self.student.full_name)

    @property
    def question_sum_common_order(self):
        return self.common_quiz_questions.count() + self.order_quiz_questions.count()

    @property
    def common_quiz_questions(self):
        """
        Returns only common quiz questions
        """
        return self.quiz_questions.filter(question__type=QUESTION_TYPES.common)

    @property
    def order_quiz_questions(self):
        """
        Returns only order quiz questions
        """
        return self.quiz_questions.filter(question__type=QUESTION_TYPES.order)

    @property
    def mapping_quiz_questions(self):
        """
        Returns only mapping quiz questions
        """
        return self.quiz_questions.filter(question__type=QUESTION_TYPES.mapping)


class QuizQuestion(TimeStampedModel):
    QUIZ_QUESTION_STATUS_TYPES = Choices(
        (0, 'active', 'Active'),
        (1, 'done', 'Done'),
        (2, 'suspend', 'Suspend'),
    )

    quiz = models.ForeignKey(Quiz, verbose_name=_('Quiz'), on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.ForeignKey(Question, verbose_name=_('Question'), on_delete=models.CASCADE,
                                 related_name='quiz_questions')
    status = models.IntegerField(_("Status"), choices=QUIZ_QUESTION_STATUS_TYPES,
                                 default=QUIZ_QUESTION_STATUS_TYPES.active)

    class Meta:
        verbose_name = _('Quiz Question')
        verbose_name_plural = _('Quiz Questions')

    def __str__(self):
        return '{}_{}'.format(self.quiz.student.full_name, self.question.id)

    @property
    def ordered_quizanswers_by_position(self):
        quizanswers_ids = self.quizanswer_set.values_list('id', flat=True)
        if self.question.type == QUESTION_TYPES.common:
            return QuizCommonAnswer.objects.filter(id__in=quizanswers_ids).order_by('number')
        elif self.question.type == QUESTION_TYPES.order:
            return QuizOrderAnswer.objects.filter(id__in=quizanswers_ids).order_by('number_2')
        if self.question.type == QUESTION_TYPES.mapping:
            return QuizMappingAnswer.objects.filter(id__in=quizanswers_ids).order_by('number_2')
        return self.quizanswer_set


class QuizAnswer(PolymorphicModel, TimeStampedModel):
    quiz_question = models.ForeignKey(QuizQuestion, verbose_name=_('Quiz Question'), on_delete=NON_POLYMORPHIC_CASCADE)
    answer = models.ForeignKey(Answer, verbose_name=_('Answer'), related_name='quiz_answers',
                               on_delete=NON_POLYMORPHIC_CASCADE)

    class Meta:
        verbose_name = _('Quiz Answer')
        verbose_name_plural = _('Quiz Answers')

    @property
    def type(self):
        return self._meta.object_name

    def __str__(self):
        return str(self.id)


class QuizCommonAnswer(QuizAnswer):
    number = models.IntegerField(_("Answer Order"), choices=CommonAnswer.ORDER_COMMON)

    class Meta:
        verbose_name = _('Quiz Common Answer')
        verbose_name_plural = _('Quiz Common Answers')


class QuizOrderAnswer(QuizAnswer):
    number_1 = models.IntegerField(_("Answer FIRST Position"), choices=OrderAnswer.ORDER_FIRST_CHAIN)
    number_2 = models.IntegerField(_("Answer SECOND Position"), choices=OrderAnswer.ORDER_SECOND_CHAIN)

    class Meta:
        verbose_name = _('Quiz Order Answer')
        verbose_name_plural = _('Quiz Order Answers')


class QuizMappingAnswer(QuizAnswer):
    number_1 = models.IntegerField(_("First chain"), choices=MappingAnswer.FIRST_CHAIN_TYPES)
    number_2 = models.IntegerField(_("Second chain"), choices=MappingAnswer.SECOND_CHAIN_TYPES)

    class Meta:
        verbose_name = _('Quiz Mapping Answer')
        verbose_name_plural = _('Quiz Mapping Answers')
