# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base.html'), name="home"),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^users/', include("centr_osvita.users.urls", namespace="users")),
    url(r'^common/', include("centr_osvita.common.urls", namespace="common")),
    # Your stuff: custom urls includes go here
]

if settings.USE_SILK:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk'))
    ]

if settings.USE_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
