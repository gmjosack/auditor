from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.db import IntegrityError, DatabaseError

import json
from models import Event
from shortcuts import r2r, json_response, normalize_post


def index(request):
    ctxt = {}
    ctxt['events'] = Event.objects.order_by('-start')

    return r2r(request, "index", ctxt)


def event(request, event_id=None):
    # Create Event
    if request.method == "POST" and event_id is None:
        try:
            event = Event(**normalize_post(request.POST))
            event.save()
            return json_response(event.to_dict())
        except IntegrityError as err:
            return json_response({"msg": str(err)}, "error", 400)
        except DatabaseError as err:
            return json_response({"msg": str(err)}, "error", 500)


    # Update Event
    if request.method == "PUT" and event_id is not None:
        try:
            event = Event.objects.get(pk=event_id)
            event.update(request.read())
            event.save()
            return json_response(event.to_dict())
        except Event.DoesNotExist as err:
            return json_response({"msg": str(err)}, "error", 404)


    #TODO(gary): View Event
    #TODO(gary): View Events

    return json_response({"msg": "Invalid Request."}, "error", 400)
