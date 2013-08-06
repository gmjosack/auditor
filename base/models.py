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
    start = models.DateTimeField(blank=True, default=aware_utcnow)
    end = models.DateTimeField(blank=True, null=True)

    def task_nums(self):
        _counts = self.task_set.values('status').annotate(Count('status'))
        counts = {"Total": 0}

        for status in _counts:
            counts["Total"] += status["status__count"]
            counts[status["status"]] = status["status__count"]

        return counts


    def to_dict(self):
        return dict(
            id = self.pk,
            summary = self.summary,
            user = self.user,
            tags = self.tags,
            start = self.start,
            end = self.end
        )

    def update(self, data):
        if isinstance(data, basestring):
            data = json.loads(data)

        valid_fields = ["end", "tags"]

        for key, value in data.iteritems():
            if key in valid_fields:
                setattr(self, key, value)

tagging.register(Event, tag_descriptor_attr="tag_list")


class Task(models.Model):
    event = models.ForeignKey(Event)
    summary = models.CharField(max_length=120)
    progress = models.PositiveSmallIntegerField(default=0, blank=True)
    status_choices = choices(("Running", "Failed", "Success"))
    status = models.CharField(max_length=30, choices=status_choices, default="Running")
    details = models.TextField()
    start = models.DateTimeField(blank=True, default=aware_utcnow)
    end = models.DateTimeField(blank=True, null=True)

    def to_dict(self):
        return serializers.serialize('json', [self])

