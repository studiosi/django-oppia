# oppia/xapi/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
        url(r'^export/$', 'oppia.xapi.views.csv_export', name="oppia_xapi_csv_export"),
        )