# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import HttpResponse


class HealthCheckView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(settings.HEALTH_CHECK_BODY, status=200)


class HomePageView(TemplateView):
    template_name = "web/home.html"


class OurTeachersView(TemplateView):
    template_name = "web/ourTeachers.html"


class StatisticsView(TemplateView):
    template_name = "web/statistics.html"


class NiceMomentView(TemplateView):
    template_name = "web/niceMoment.html"


class CenterAlisaView(TemplateView):
    template_name = "web/alisa.html"


class ZNOAdvicesView(TemplateView):
    template_name = "web/zno_advices.html"


class ContactsView(TemplateView):
    template_name = "web/contacts.html"
