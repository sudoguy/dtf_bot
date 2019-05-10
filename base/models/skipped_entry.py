from .base import BaseModel
from django.db import models


class SkippedEntry(BaseModel):
    id = models.BigIntegerField(primary_key=True)
