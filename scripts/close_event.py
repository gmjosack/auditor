#!/usr/bin/env python

import sys

import requests
from pytz import UTC
from datetime import datetime
import json

event_id = sys.argv[1]

headers = {'Content-type': 'application/json'}

r = requests.put("http://localhost:8000/event/%s/" % event_id, data=json.dumps({
    "end": str(UTC.localize(datetime.utcnow())),
    #"tags": "tets",
}), headers=headers )

print r.text
