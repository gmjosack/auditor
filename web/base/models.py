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

