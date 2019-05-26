from .base import BaseModel
from django.db import models
from django.contrib.postgres.fields import JSONField


class User(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    created = models.IntegerField(null=True)
    name = models.CharField(max_length=255)

    url = models.TextField()
    avatar_url = models.CharField(max_length=255, null=True)

    karma = models.IntegerField(null=True)
    user_hash = models.CharField(max_length=255, null=True)
    last_response = JSONField()
