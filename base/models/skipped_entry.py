from django.db import models

from .base import BaseModel


class SkippedEntry(BaseModel):
    id = models.BigIntegerField(primary_key=True)
