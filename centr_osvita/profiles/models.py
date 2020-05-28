from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    full_name = models.CharField(_('full name'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    mother_full_name = models.CharField(_('Mother fullname'), max_length=255, null=True, blank=True,
                                        help_text=_('Maximum length is 255 symbols'))
    mother_phone = PhoneNumberField(_('Mother phone'), null=True, blank=True)
    father_full_name = models.CharField(_('Father fullname'), max_length=255, null=True, blank=True,
                                        help_text=_('Maximum length is 255 symbols'))
    father_phone = PhoneNumberField(_('Father phone'), null=True, blank=True)
    school_name = models.CharField(_('School name'), max_length=255, help_text=_('Maximum length is 255 symbols'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
