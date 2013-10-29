
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.db import IntegrityError, DatabaseError

import pika
import json
from models import Event, Attribute, Stream
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

    # View Events
    if request.method == "GET" and event_id is None:
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 50))

        events = Event.objects.order_by("-start")[offset:limit]
        return json_response({"events": [event.to_dict() for event in events]})

    # View Event
    if request.method == "GET" and event_id:
        event = Event.objects.get(pk=event_id)
        return json_response(event.to_dict())

    return json_response({"msg": "Invalid Request."}, "error", 400)


def event_details(request, event_id=None):
    # Set a detail/attribute
    if request.method == "POST":
        try:
            event = Event.objects.get(pk=event_id)
            data = json.loads(request.read())

            payload = {
                "event_id": event.id,
                "details": [],
            }

            for detail in data["details"]:
                details_type = detail["details_type"]
                key = detail["name"]
                value = detail["value"]
                mode = detail["mode"]

                if details_type == "attribute":
                    attributes = Attribute.objects.filter(event=event, key=key)
                    if not attributes or mode == "append":
                        attribute = Attribute(event=event, key=key, value=value)
                        attribute.save()
                    elif mode == "set":
                        for attribute in attributes[1:]:
                            attribute.delete()
                        attribute = attributes[0]
                        attribute.value = value
                        attribute.save()

                elif details_type == "stream":
                    stream = Stream.objects.filter(event=event, name=key)
                    if stream:
                        stream = stream.get()
                        stream_text = value
                        if mode == "append":
                            stream_text = stream.text + stream_text
                        stream.text = stream_text
                    else:
                        stream = Stream(event=event, name=key, text=value)
                    stream.save()

                payload["details"].append(detail)

            publish("event_details", "update", payload, event_id=event.id)
            return json_response({"msg": ""})

        except IntegrityError as err:
            return json_response({"msg": str(err)}, "error", 400)
        except DatabaseError as err:
            return json_response({"msg": str(err)}, "error", 500)


    # Get Details for an event
    if request.method == "GET":
        try:
            data = {}
            event = Event.objects.get(pk=event_id)
            data["event_id"] = event.id
            data["attributes"] = event.attributes()
            data["streams"] = [stream.to_dict() for stream in event.streams()]
            return json_response(data)
        except Event.DoesNotExist as err:
            return json_response({"msg": str(err)}, "error", 404)

