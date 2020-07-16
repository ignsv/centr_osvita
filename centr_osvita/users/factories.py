import factory

from django.utils import lorem_ipsum
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    @factory.lazy_attribute_sequence
    def username(self, n):
        return '+{}'.format(n + 380970000000)

    @factory.lazy_attribute
    def email(self):
        return '{}@dumpy.com'.format(self.username)

    @factory.lazy_attribute
    def phone(self):
        return self.username

    @factory.lazy_attribute_sequence
    def first_name(self, n):
        return '{0}_{1}@example.com'.format(lorem_ipsum.words(1, False), n)

    @factory.lazy_attribute_sequence
    def last_name(self, n):
        return '{0}_{1}@example.com'.format(lorem_ipsum.words(1, False), n)

    @factory.lazy_attribute_sequence
    def password(self, n):
        return make_password('12345678')

    is_active = True
