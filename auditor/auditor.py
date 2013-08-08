#!/usr/bin/env python

import json
import os
import pytz
import requests

from datetime import datetime


#TODO(gary): subscribe method


class Event(object):
    def __init__(self, payload):
        self._update(payload)

    def _put(self, key, value, handler):
        headers = {'Content-type': 'application/json'}
        response = requests.put(
            "http://localhost:8000%s" % (handler,),
            data=json.dumps({key: value}),
            headers=headers
        )
        data = json.loads(response.text)
        if data["type"] == "error":
            raise Error(data["data"]["msg"])
        return data["data"]

    def _post(self, key, value, handler):
        headers = {'Content-type': 'application/json'}
        response = requests.post(
            "http://localhost:8000%s" % (handler,),
            data=json.dumps({key: value}),
            headers=headers
        )
        data = json.loads(response.text)
        if data["type"] == "error":
            raise Error(data["data"]["msg"])
        return data["data"]

    def set_key_value(self, key, value):
        """Sets a dynamic key/value. Fails if used on key with multiple values."""
        self._post("sd", {str(key): str(value)}, "/event/%s/details/" % self.id)

    def add_key_value(self, key, value):
        """Used to append values to a key. These values are considered immutable."""
        self._put("sd", {str(key): str(value)}, "/event/%s/details/" % self.id)

    def set_details(self, details):
        """Used to append values to a key. These values are considered immutable."""
        self._post("details", details, "/event/%s/details/" % self.id)

    def add_details(self, details):
        """Used to append values to a key. These values are considered immutable."""
        self._put("details", details, "/event/%s/details/" % self.id)

    def _update(self, payload):
        self.id = payload.get("id")
        self.summary = payload.get("summary")
        self.user = payload.get("user")
        self.tags = payload.get("tags", "").split(", ")
        self.start = payload.get("start")
        self.end = payload.get("end")

    def close(self):
        self._update(self._put("end", str(pytz.UTC.localize(datetime.utcnow())), "/event/%s/" % self.id))


class Error(Exception):
    pass


def get_user(user=None):
    if user is not None:
        return user
    if "SUDO_USER" in os.environ:
        return "%s(%s)" % (os.environ["USER"], os.environ["SUDO_USER"])
    return os.environ["USER"]



def alog(summary, tags="", user=None, level=1, end_now=True):
    data = {
        "summary": summary,
        "user": get_user(user),
        "level": level,
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


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Log or Retreive and event.")

    parser.add_argument("message", nargs="*", default=None,
                        help="A message to log to Auditor")

    parser.add_argument('--limit', default=15, type=int, help='The amount of records to return.')
    parser.add_argument('--offset', default=0, type=int, help='The offset for records to return.')
    parser.add_argument('--tags', default=[], action="append", help='Which tag to apply to message or filter.')
    parser.add_argument('--user', default="", help='Which tag to apply to message or filter.')
    parser.add_argument('--level', default=None, type=int, help='Which level to apply to message or filter')

    args = parser.parse_args()

    if args.message:
        alog_args = {}

        if args.level is not None: alog_args["level"] = args.level
        if args.user: alog_args["user"] = args.user
        if args.tags:
            new_tags = []
            for tag in args.tags:
                new_tags.extend(tag.split(","))
            alog_args["tags"] = new_tags

        alog(" ".join(args.message), **alog_args)

if __name__ == "__main__":
    main()
