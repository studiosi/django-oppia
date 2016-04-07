# oppia/xapi/views.py
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Badge, Award, AwardCourse


def csv_export(request):

    return render_to_response('oppia/reports/completion_rates.html',
                              {},
                              context_instance=RequestContext(request))