from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import json
import datetime
import pika
from django.utils.timezone import utc


def r2r(request, template, payload=None):
    if payload is None:
        payload = {}
    if not template.endswith(".html"):
        template += ".html"
    return render_to_response(
        template, payload, context_instance=RequestContext(request))


def json_response(data, type="response", status=200):
    return HttpResponse(json.dumps({"type": type, "data": data}, cls=DjangoJSONEncoder), content_type="application/json", status=status)


def choices(seq):
    return zip(seq, seq)


def normalize_post(data):
    new_data = {}
    for key, value in data.iteritems():
        if isinstance(value, list):
            new_data[key] = ", ".join(value)
        else:
            new_data[key] = value
    return new_data


def aware_utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def publish(type, cmd, data, tags=None, event_id=None):
    connection = pika.BlockingConnection()
    channel = connection.channel()

    fields = {
        "ns": "auditor",
        "type": type,
        "cmd": cmd,
    }

    if event_id is not None:
        fields["event_id"] = str(event_id)

    if tags:
        for tag in tags:
            fields["tag_%s" % tag] = "1"

    channel.basic_publish(exchange='amq.headers',
                          routing_key="",
                          body=json.dumps(data, cls=DjangoJSONEncoder),
                          properties=pika.BasicProperties(headers = fields)
    )
    connection.close()

