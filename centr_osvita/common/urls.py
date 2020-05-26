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
]
