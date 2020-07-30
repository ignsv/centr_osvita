# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^teachers/$', views.OurTeachersView.as_view(), name='teachers'),
    url(r'^statistics/$', views.StatisticsView.as_view(), name='statistics'),
    url(r'^nice-moment/$', views.NiceMomentView.as_view(), name='nice_moment'),
    url(r'^alisa/$', views.CenterAlisaView.as_view(), name='center_alisa'),
    url(r'^zno-advices/$', views.ZNOAdvicesView.as_view(), name='zno_advices'),
    url(r'^contacts/$', views.ContactsView.as_view(), name='contacts'),
    url(r'^checker/$', views.HealthCheckView.as_view()),
    url(r'^math/$', views.MathView.as_view(), name='math'),
    url(r'^ukrainian/$', views.UkrainianView.as_view(), name='ukrainian'),
    url(r'^english/$', views.EnglishView.as_view(), name='english'),
    url(r'^history/$', views.HistoryView.as_view(), name='history'),
    url(r'^physics/$', views.PhysicsView.as_view(), name='physics'),
    url(r'^geography/$', views.GeographyView.as_view(), name='geography'),
    url(r'^biology/$', views.BiologyView.as_view(), name='biology'),
    url(r'^chemistry/$', views.ChemistryView.as_view(), name='chemistry'),
]
