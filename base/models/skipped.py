from django.db import models

from .base import BaseModel


class Skipped(BaseModel):
    object_id = models.BigIntegerField()
    object_type = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["object_id", "object_type"], name="unique_skipped")
        ]
