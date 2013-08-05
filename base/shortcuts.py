from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

import json

def r2r(request, template, payload=None):
    if payload is None:
        payload = {}
    if not template.endswith(".html"):
        template += ".html"
    return render_to_response(
        template, payload, context_instance=RequestContext(request))

def json_response(data, status=200):
    return HttpResponse(json.dumps(data), content_type="application/json", status=status)
