#!/usr/bin/env python

import requests
from pytz import UTC
from datetime import datetime

r = requests.post("http://localhost:8000/event/", data={
    "summary": "dsh -Mcg nginx sudo kick",
    "user": "gary",
    "tags": "kick, dsh",
#    "start": UTC.localize(datetime.utcnow()),
})

print r.text
