import uuid

from django.db import models


TYPE_IMAGE, TYPE_VIDEO, TYPE_AUDIO, TYPE_FILE = (
    'image', 'video', 'audio', 'file')


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        (TYPE_IMAGE, TYPE_IMAGE),
        (TYPE_VIDEO, TYPE_VIDEO),
        (TYPE_AUDIO, TYPE_AUDIO),
        (TYPE_FILE, TYPE_FILE),
    )

    file = models.FileField(upload_to='media')
    type = models.CharField(max_length=6, choices=MEDIA_TYPE_CHOICES)
