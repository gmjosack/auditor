import json
from datetime import datetime

from django.db.models import Count
from django.core import serializers
from django.db import models
from tagging.fields import TagField

import tagging

from shortcuts import choices, aware_utcnow

class Event(models.Model):
    summary = models.CharField(max_length=120)
    user = models.CharField(max_length=120)
    tags = TagField(blank=True, null=True)
    level = models.PositiveSmallIntegerField(blank=True, default=1)
    start = models.DateTimeField(blank=True, default=aware_utcnow)
    end = models.DateTimeField(blank=True, null=True)

    def to_dict(self):
        return dict(
            id = self.pk,
            summary = self.summary,
            user = self.user,
            tags = self.tags,
            level = self.level,
            start = self.start,
            end = self.end
        )

    def attributes(self, key=None):
        data = {}
        attributes = self.attribute_set.all()
        for item in attributes:
            if key and key != item.key:
                continue
            if item.key in data:
                last_value = data[item.key]
                if not isinstance(last_value, list):
                    data[item.key] = [last_value]
                data[item.key].append(item.value)
            else:
                data[item.key] = item.value
        return data

    def streams(self):
        return Stream.objects.filter(event=self)

    def update(self, data):
        if isinstance(data, basestring):
            data = json.loads(data)

        valid_fields = ["end", "tags"]

        for key, value in data.iteritems():
            if key in valid_fields:
                setattr(self, key, value)
tagging.register(Event, tag_descriptor_attr="tag_list")


class Attribute(models.Model):
    event = models.ForeignKey(Event)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=60)

    def __unicode__(self):
        return "Key: %s, Value: %s" % (self.key, self.value)


class Stream(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=20)
    text = models.TextField(blank=True, null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event.id,
            "name": self.name,
            "text": self.text,
        }

