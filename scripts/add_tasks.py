#!/usr/bin/env python

import requests
from pytz import UTC
from datetime import datetime
import json


headers = {'Content-type': 'application/json'}

data = []

for i in range(1000):
    data.append({"summary": "host%s" % i})

r = requests.post("http://localhost:8000/event/3/task/", data=json.dumps(data), headers=headers)

print r.text
