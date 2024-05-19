from django.db import models
from config.settings.base import MEDIA_ROOT


class IngestStatus(models.TextChoices):
    PENDING = ("pending", "Pending")
    FAILED = ("failed", "Failed")
    PROCESSING = ("processing", "Processing")
    COMPLETE = ("complete", "Complete")


class Ingest(models.Model):
    text_data = models.TextField()
    file = models.FileField(upload_to="ingest/uploads/", null=True, blank=True, default=None)
    status = models.CharField(
        max_length=16, choices=IngestStatus.choices, default=IngestStatus.PENDING
    )

    def __str__(self):
        return f"Ingest {self.id}"
