from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import Comment, Entry
from base.tasks import update_entry


class NewComment(APIView):
    def post(self, request):
        data = request.data["data"]

        entry_id = data["content"]["id"]

        try:
            entry = Entry.objects.get(id=entry_id)
        except ObjectDoesNotExist:
            update_entry(entry_id)
            entry = Entry.objects.get(id=entry_id)

        new_comment = Comment(
            id=data["id"],
            text=data["text"],
            reply_to=data["reply_to"] or data["reply_to"]["id"],
            last_response=data,
            entry=entry,
        )
        new_comment.save()

        return Response()
