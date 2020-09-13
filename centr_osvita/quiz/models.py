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
    return 'test_{0}/{1}'.format(str(instance.test.id),
                                    filename[:dot_position]+str(int(time.time()))+filename[dot_position:])


class Subject(models.Model):
    name = models.CharField(_('Subject name'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    slug = models.SlugField(_('Slug name'))

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return self.name

    @property
    def ordered_statistic_by_year(self):
        return self.statistics.order_by('year__date')


class Year(models.Model):
    date = models.SmallIntegerField(_('Year info'))

    def __str__(self):
        return str(self.date)


class YearSubjectStatistics(models.Model):
    subject = models.ForeignKey(Subject, verbose_name=_('Subject'), on_delete=models.CASCADE, related_name='statistics')
    percent_c = models.IntegerField(_('Percent of pupils that have C mark'))
    percent_b = models.IntegerField(_('Percent of pupils that have B mark'))
    percent_a = models.IntegerField(_('Percent of pupils that have A mark'))
    year = models.ForeignKey(Year, verbose_name=_('Year'), on_delete=models.CASCADE, related_name='statistics')


class TestParameter(TimeStampedModel):
    test_time = models.SmallIntegerField(_('Test time'), default=20)
    number_of_common_questions =  models.SmallIntegerField(_('Number of common questions'))
    number_of_order_questions = models.SmallIntegerField(_('Number of order questions'))
    number_of_mapping_questions = models.SmallIntegerField(_('Number of mapping questions'))
    coefficient_of_common_question = models.FloatField(_('coefficient per common questions'))
    coefficient_of_order_question = models.FloatField(_('coefficient per order questions'))
    coefficient_of_mapping_question = models.FloatField(_('coefficient per mapping questions'))

    class Meta:
        verbose_name = _('Test Parameter')


class Test(TimeStampedModel):
    subject = models.ForeignKey(Subject, verbose_name=_('Subject'), on_delete=models.CASCADE, related_name='tests')
    name = models.CharField(_('Test name'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    status = models.BooleanField(_('Publish status'))
    test_parameter = models.OneToOneField(TestParameter, verbose_name=_('Test Parameter'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')

    def __str__(self):
        return '{} {}'.format(self.subject.name, self.name)

class Question(TimeStampedModel):
    test = models.ForeignKey(Test, verbose_name=_('Test'), on_delete=models.CASCADE, related_name='questions')
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

    @property
    def ordered_answers_by_position_two(self):
        answers_ids = self.answer_set.values_list('id', flat=True)
        if self.type == QUESTION_TYPES.common:
            return CommonAnswer.objects.filter(id__in=answers_ids).order_by('number')
        elif self.type == QUESTION_TYPES.order:
            return OrderAnswer.objects.filter(id__in=answers_ids).order_by('number_2')
        if self.type == QUESTION_TYPES.mapping:
            return MappingAnswer.objects.filter(id__in=answers_ids).order_by('number_2')
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
        (5, 'fifth', 'E'),
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
    test = models.ForeignKey(Test, verbose_name=_('Test'), on_delete=models.CASCADE, related_name='quizzes')
    status = models.IntegerField(_("Status"), choices=QUIZ_STATUS_TYPES, default=QUIZ_STATUS_TYPES.progress)
    student = models.ForeignKey(Profile, verbose_name=_('Student'), on_delete=models.CASCADE, related_name='quizzes')

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    def __str__(self):
        return '{}:{}_{}'.format(self.id, self.test.name, self.student.full_name)

    def create_random_quiz_questions(self):
        common_questions = Question.objects.filter(
            test=self.test,
            type=QUESTION_TYPES.common).order_by('?')[:self.test.test_parameter.number_of_common_questions]
        order_questions = Question.objects.filter(
            test=self.test,
            type=QUESTION_TYPES.order).order_by('?')[:self.test.test_parameter.number_of_order_questions]
        mapping_questions = Question.objects.filter(
            test=self.test,
            type=QUESTION_TYPES.mapping).order_by('?')[:self.test.test_parameter.number_of_mapping_questions]

        for common in common_questions:
            QuizQuestion.objects.create(question=common, quiz=self)

        for order in order_questions:
            QuizQuestion.objects.create(question=order, quiz=self)

        for mapping in mapping_questions:
            QuizQuestion.objects.create(question=mapping, quiz=self)


    @property
    def question_sum_common_order(self):
        return self.common_quiz_questions.count() + self.order_quiz_questions.count()

    @property
    def max_available_mark(self):
        max_mark = self.common_quiz_questions.count()*self.test.test_parameter.coefficient_of_common_question \
                   + self.order_quiz_questions.count()*self.test.test_parameter.coefficient_of_order_question*3
        for quiz_mapping_question in self.mapping_quiz_questions:
            max_mark += quiz_mapping_question.question.ordered_answers_by_position.exclude(
                number_1=MappingAnswer.FIRST_CHAIN_TYPES.zero).count()*self.test.test_parameter.coefficient_of_mapping_question
        return round(max_mark, 2)

    @property
    def current_mark(self):
        result_mark = 0
        for common_quiz_question in self.common_quiz_questions:
            for quiz_answer in common_quiz_question.quizanswer_set.all():
                if quiz_answer.answer.correct and quiz_answer.answer.number == quiz_answer.number:
                    result_mark += self.test.test_parameter.coefficient_of_common_question

        for order_quiz_question in self.order_quiz_questions:
            in_row = True
            for index, quiz_answer in enumerate(order_quiz_question.ordered_quizanswers_by_position_one):
                if not in_row and index == order_quiz_question.quizanswer_set.count()-1 \
                        and quiz_answer.answer.number_1 == quiz_answer.number_1 \
                        and quiz_answer.answer.number_2 == quiz_answer.number_2:
                    result_mark += self.test.test_parameter.coefficient_of_order_question
                elif in_row and index == order_quiz_question.quizanswer_set.count()-1 \
                        and quiz_answer.answer.number_1 == quiz_answer.number_1 \
                        and quiz_answer.answer.number_2 == quiz_answer.number_2:
                    pass
                elif in_row and quiz_answer.answer.number_1 == quiz_answer.number_1 \
                        and quiz_answer.answer.number_2 == quiz_answer.number_2:
                    result_mark += self.test.test_parameter.coefficient_of_order_question
                else:
                    in_row = False

        for mapping_quiz_question in self.mapping_quiz_questions:
            for quiz_answer in mapping_quiz_question.ordered_quizanswers_by_position_one:
                if quiz_answer.answer.number_1 == quiz_answer.number_1 \
                        and quiz_answer.answer.number_1 != MappingAnswer.FIRST_CHAIN_TYPES.zero \
                        and quiz_answer.answer.number_2 == quiz_answer.number_2:
                    result_mark += self.test.test_parameter.coefficient_of_mapping_question

        return round(result_mark, 2)

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
        return '{}:{}_{}'.format(self.id, self.quiz.student.full_name, self.question.id)

    @property
    def ordered_quizanswers_by_position_two(self):
        quizanswers_ids = self.quizanswer_set.values_list('id', flat=True)
        if self.question.type == QUESTION_TYPES.common:
            return QuizCommonAnswer.objects.filter(id__in=quizanswers_ids).order_by('number')
        elif self.question.type == QUESTION_TYPES.order:
            return QuizOrderAnswer.objects.filter(id__in=quizanswers_ids).order_by('number_2')
        if self.question.type == QUESTION_TYPES.mapping:
            return QuizMappingAnswer.objects.filter(id__in=quizanswers_ids).order_by('number_2')
        return self.quizanswer_set

    @property
    def ordered_quizanswers_by_position_one(self):
        quizanswers_id_list = self.quizanswer_set.values_list('id', flat=True)
        if self.question.type == QUESTION_TYPES.common:
            return QuizCommonAnswer.objects.filter(id__in=quizanswers_id_list).order_by('number')
        elif self.question.type == QUESTION_TYPES.order:
            return QuizOrderAnswer.objects.filter(id__in=quizanswers_id_list).order_by('number_1')
        if self.question.type == QUESTION_TYPES.mapping:
            return QuizMappingAnswer.objects.filter(id__in=quizanswers_id_list).order_by('number_1')
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
