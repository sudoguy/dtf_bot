from .base import BaseModel
from django.db import models
from django.contrib.postgres.fields import JSONField


class Entry(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    intro = models.CharField(max_length=512)
    last_response = JSONField()
