
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.db import IntegrityError, DatabaseError

import pika
import json
from models import Event, StructuredData
from shortcuts import r2r, json_response, normalize_post, publish

import logging
logging.basicConfig()


def index(request):
    ctxt = {}

    page = request.GET.get("page", 1)
    limit = int(request.GET.get("limit", 50))
    event_list = Event.objects.order_by('-start')
    paginator = Paginator(event_list, limit)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    ctxt['events'] = events
    ctxt['limit'] = limit
    ctxt['page'] = int(page)
    ctxt['num_pages'] = int(paginator.num_pages)

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

            if "sd" in data:
                key = data["sd"].keys()[0]
                value = data["sd"].get(key)

                attributes = StructuredData.objects.filter(event=event, key=key)

                if not attributes:
                    attribute = StructuredData(event=event, key=key, value=value)
                    attribute.save()
                elif len(attributes) == 1:
                    attribute = attributes[0]
                    attribute.value = value
                    attribute.save()
                else:
                    return json_response({"msg": "Tried to set attribute with more than one value."}, "error", 400)

                payload = {
                    "type": "sd",
                    "op_type": "set",
                    "event_id": event.id,
                    "data": {key: value},
                }
                publish("event_details", "new", payload, event_id=event.id)
                return json_response({"msg": ""})

            elif "details" in data:
                event.details = data["details"]
                event.save()
                payload = {
                    "type": "details",
                    "op_type": "set",
                    "event_id": event.id,
                    "data": event.details,
                }
                publish("event_details", "new", payload, event_id=event.id)
                return json_response({"msg": ""})

            return json_response({"msg": str(err)}, "error", 400)
        except IntegrityError as err:
            return json_response({"msg": str(err)}, "error", 400)
        except DatabaseError as err:
            return json_response({"msg": str(err)}, "error", 500)


    # Update details/attribute
    if request.method == "PUT":
        try:
            event = Event.objects.get(pk=event_id)
            data = json.loads(request.read())

            if "sd" in data:
                key = data["sd"].keys()[0]
                value = data["sd"].get(key)


                attribute = StructuredData(event=event, key=key, value=value)
                attribute.save()

                payload = {
                    "type": "sd",
                    "op_type": "append",
                    "event_id": event.id,
                    "data": {key: value},
                }
                publish("event_details", "append", payload, event_id=event.id)
                return json_response({"msg": ""})

            elif "details" in data:
                if event.details:
                    event.details = event.details + data["details"]
                else:
                    event.details = data["details"]
                event.save()
                payload = {
                    "type": "details",
                    "op_type": "append",
                    "event_id": event.id,
                    "data": data["details"],
                }
                publish("event_details", "append", payload, event_id=event.id)
                return json_response({"msg": ""})

            return json_response({"msg": str(err)}, "error", 400)
        except IntegrityError as err:
            return json_response({"msg": str(err)}, "error", 400)
        except DatabaseError as err:
            return json_response({"msg": str(err)}, "error", 500)

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
