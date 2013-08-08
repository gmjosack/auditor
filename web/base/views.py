from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.db import IntegrityError, DatabaseError

import pika
import json
from models import Event
from shortcuts import r2r, json_response, normalize_post, publish

import logging
logging.basicConfig()


def index(request):
    ctxt = {}
    ctxt['events'] = Event.objects.order_by('-start')[:50]

    return r2r(request, "index", ctxt)


def event(request, event_id=None):
    # Create Event
    if request.method == "POST" and event_id is None:
        try:
            event = Event(**normalize_post(request.POST))
            event.save()
            data = event.to_dict()
            publish("event", "new", data, tags=event.tag_list)
            return json_response(data)
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
            data = event.to_dict()
            publish("event", "update", data, tags=event.tag_list)
            return json_response(data)
        except Event.DoesNotExist as err:
            return json_response({"msg": str(err)}, "error", 404)


    #TODO(gary): View Event
    #TODO(gary): View Events

    return json_response({"msg": "Invalid Request."}, "error", 400)


def event_details(request, event_id=None):
    # Set a detail/attribute
    if request.method == "POST":
        try:
            event = Event.objects.get(pk=event_id)
            data = json.loads(request.read())

            #publish("event_details", "new", data)
            return json_response({})
        except IntegrityError as err:
            return json_response({"msg": str(err)}, "error", 400)
        except DatabaseError as err:
            return json_response({"msg": str(err)}, "error", 500)


    # Update details/attribute
    if request.method == "PUT":
        try:
            event = Event.objects.get(pk=event_id)
            data = json.loads(request.read())

            #publish("event_details", "update", data)
            return json_response({})
        except Event.DoesNotExist as err:
            return json_response({"msg": str(err)}, "error", 404)

    # Get Details for an event
    if request.method == "GET":
        try:
            data = {}
            event = Event.objects.get(pk=event_id)
            data["sd"] = event.structured_data()
            data["details"] = event.details
            return json_response(data)
        except Event.DoesNotExist as err:
            return json_response({"msg": str(err)}, "error", 404)
