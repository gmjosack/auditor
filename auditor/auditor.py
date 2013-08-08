
import json
import os
import pytz
import requests

from datetime import datetime


#TODO(gary): subscribe method


class Event(object):
    def __init__(self, payload):
        self._update(payload)

    def _put(self, key, value):
        headers = {'Content-type': 'application/json'}
        response = requests.put(
            "http://localhost:8000/event/%s/" % self.id,
            data=json.dumps({key: value}),
            headers=headers
        )
        data = json.loads(response.text)
        if data["type"] == "error":
            raise Error(data["data"]["msg"])
        return data["data"]

    def _update(self, payload):
        self.id = payload.get("id")
        self.summary = payload.get("summary")
        self.user = payload.get("user")
        self.tags = payload.get("tags", []).split(", ")
        self.start = payload.get("start")
        self.end = payload.get("end")

    def close(self):
        self._update(self._put("end", str(pytz.UTC.localize(datetime.utcnow()))))


class Error(Exception):
    pass


def get_user(user=None):
    if user is not None:
        return user
    if "SUDO_USER" in os.environ:
        return "%s(%s)" % (os.environ["USER"], os.environ["SUDO_USER"])
    return os.environ["USER"]



def alog(summary, tags="", user=None, end_now=True):
    data = {
        "summary": summary,
        "user": get_user(user),
        "start": pytz.UTC.localize(datetime.utcnow()),
    }

    if isinstance(tags, list):
        tags = ", ".join(tags)
    if tags: data["tags"] = tags

    if end_now:
        data["end"] = data["start"]

    response = json.loads(requests.post("http://localhost:8000/event/", data=data).text)

    if response["type"] == "error":
        raise Error(response["data"]["msg"])

    return Event(response["data"])

