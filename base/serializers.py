from rest_framework.serializers import (
    Serializer,
    CharField,
    ChoiceField,
    IntegerField,
    JSONField,
    URLField,
    UUIDField,
)


class ImageSerializer(Serializer):
    uuid = UUIDField()
    width = IntegerField()
    height = IntegerField()
    size = IntegerField()
    type = CharField()
    color = CharField()


IMAGE = "image"
VIDEO = "video"
MEDIA_CHOICES = ((IMAGE, "Image"), (VIDEO, "Video"))


class MediaSerializer(Serializer):
    type = ChoiceField(choices=MEDIA_CHOICES)


class CommentSerializer(Serializer):
    id = IntegerField()
    url = URLField()
    text = CharField()
    author = JSONField()
