# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager
from centr_osvita.profiles.models import Profile


class ProfileUserManager(BaseUserManager):
    def create_user(self, phone, password):
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone=phone,
            username=phone,
            email=phone+'@dumpy.com'
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        create superuser with dumpy phone and profile
        """
        user = self.model(
            phone='+380971111111',  # dumpy phone number
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        Profile.objects.create(user=user, full_name='Admin Admin', school_name='Admin')
        return user


class User(AbstractUser):
    phone = PhoneNumberField(unique=True)

    objects = ProfileUserManager()

    def __str__(self):
        return self.phone.as_e164
