
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


    if request.method == "GET" and event_id is None:
        pass
    #TODO(gary): View Event
    #TODO(gary): View Events


    return json_response({"msg": "Invalid Request."}, "error", 400)


def event_details(request, event_id=None):
    # Set a detail/attribute
    if request.method == "POST":
        try:
            event = Event.objects.get(pk=event_id)
            data = json.loads(request.read())

            if "attribute" in data:
                key = data["attribute"].keys()[0]
                value = data["attribute"].get(key)

                attributes = Attribute.objects.filter(event=event, key=key)

                if not attributes:
                    attribute = Attribute(event=event, key=key, value=value)
                    attribute.save()
                elif len(attributes) == 1:
                    attribute = attributes[0]
                    attribute.value = value
                    attribute.save()
                else:
                    return json_response({"msg": "Tried to set attribute with more than one value."}, "error", 400)

                payload = {
                    "type": "attribute",
                    "op_type": "set",
                    "event_id": event.id,
                    "data": {key: value},
                }
                publish("event_details", "new", payload, event_id=event.id)
                return json_response({"msg": ""})

            elif "stream" in data:
                stream_name = data["stream"]["name"]
                stream_text = data["stream"]["text"]
                stream = Stream.objects.filter(event=event, name=stream_name)
                if stream:
                    stream = stream.get()
                    stream.text = stream_text
                else:
                    stream = Stream(event=event, name=stream_name, text=stream_text)
                stream.save()
                payload = {
                    "type": "stream",
                    "op_type": "set",
                    "event_id": event.id,
                    "data": data["stream"],
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

            if "attribute" in data:
                key = data["attribute"].keys()[0]
                value = data["attribute"].get(key)


                attribute = Attribute(event=event, key=key, value=value)
                attribute.save()

                payload = {
                    "type": "attribute",
                    "op_type": "append",
                    "event_id": event.id,
                    "data": {key: value},
                }
                publish("event_details", "append", payload, event_id=event.id)
                return json_response({"msg": ""})

            elif "stream" in data:
                stream_name = data["stream"]["name"]
                stream = Stream.objects.filter(event=event, name=stream_name)
                if stream:
                    stream = stream.get()
                    stream.text = stream.text + data["stream"]["text"]
                else:
                    stream = Stream(event=event, name=stream_name, text=data["stream"]["text"])
                stream.save()
                payload = {
                    "type": "stream",
                    "op_type": "append",
                    "event_id": event.id,
                    "data": data["stream"],
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
            data["event_id"] = event.id
            data["attributes"] = event.attributes()
            data["streams"] = [stream.to_dict() for stream in event.streams()]
            return json_response(data)
        except Event.DoesNotExist as err:
            return json_response({"msg": str(err)}, "error", 404)

