from .base import BaseModel
from .entry import Entry
from django.db import models
from django.contrib.postgres.fields import JSONField


OTHER, ANDROID, IOS = range(3)
SOURCE_CHOICES = ((OTHER, "Other"), (ANDROID, "Android"), (IOS, "iOS"))


class Comment(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    text = models.TextField()
    reply_to = models.IntegerField()

    is_favorited = models.BooleanField()
    is_pinned = models.BooleanField()
    is_edited = models.BooleanField()

    level = models.SmallIntegerField()
    source_id = models.SmallIntegerField(choices=SOURCE_CHOICES)
    last_response = JSONField()

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
