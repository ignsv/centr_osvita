import factory

from django.apps import apps
from centr_osvita.users.factories import UserFactory
from django.utils import lorem_ipsum

Profile = apps.get_model('profiles', 'Profile')


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

    @factory.lazy_attribute_sequence
    def full_name(self, n):
        return '{0} {1}@example.com'.format(lorem_ipsum.words(1, False), n)

    @factory.lazy_attribute_sequence
    def parent_full_name(self, n):
        return '{0} {1}@example.com'.format(lorem_ipsum.words(1, False), n)

    @factory.lazy_attribute_sequence
    def parent_phone(self, n):
        return '+{}'.format(n + 380980000000)

    @factory.lazy_attribute_sequence
    def institution_name(self, n):
        return '{0} {1}@example.com'.format(lorem_ipsum.words(1, False), n)

    grade = Profile.GRADE_NUMBER.nine
