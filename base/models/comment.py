from .base import BaseModel
from .entry import Entry
from django.db import models
from django.contrib.postgres.fields import JSONField


OTHER, ANDROID, IOS = range(3)
UNKNOWN = None
SOURCE_CHOICES = ((OTHER, "Other"), (ANDROID, "Android"), (IOS, "iOS"), (UNKNOWN, "Unknown"))


class Comment(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    text = models.TextField()
    reply_to = models.IntegerField(null=True)

    is_favorited = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    level = models.SmallIntegerField()
    source_id = models.SmallIntegerField(choices=SOURCE_CHOICES, null=True, default=UNKNOWN)
    last_response = JSONField()

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
