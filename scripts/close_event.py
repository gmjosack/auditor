#!/usr/bin/env python

import sys
import pika

import logging
logging.basicConfig()


import requests
from pytz import UTC
from datetime import datetime
import json

event_id = sys.argv[1]

connection = pika.BlockingConnection()
channel = connection.channel()

headers = {'Content-type': 'application/json'}

r = requests.put("http://localhost:8000/event/%s/" % event_id, data=json.dumps({
    "end": str(UTC.localize(datetime.utcnow())),
}), headers=headers )


x = json.loads(r.text)

if x["type"] == "response":
    channel.basic_publish(exchange='amq.topic',
                          routing_key='event.update',
                          body=json.dumps(x["data"])
    )

channel.close()
connection.close()


