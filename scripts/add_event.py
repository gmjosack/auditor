#!/usr/bin/env python

import json
import requests
import pika
from pytz import UTC
from datetime import datetime

import logging
logging.basicConfig()


connection = pika.BlockingConnection()
channel = connection.channel()


r = requests.post("http://localhost:8000/event/", data={
    "summary": "dsh -Mcg nginx sudo kick",
    "user": "gary",
    "tags": "kick, dsh",
#    "start": UTC.localize(datetime.utcnow()),
})

x = json.loads(r.text)

if x["type"] == "response":
    channel.basic_publish(exchange='amq.topic',
                          routing_key='event.new',
                          body=json.dumps(x["data"])
    )

channel.close()
connection.close()

