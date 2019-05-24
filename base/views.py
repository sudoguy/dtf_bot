from rest_framework.views import APIView
from rest_framework.response import Response

from base.models import Comment, Entry


class NewComment(APIView):
    def post(self, request):
        data = request.data["data"]

        entry = Entry.objects.get(data["content"]["id"])

        new_comment = Comment(
            id=data["id"],
            text=data["text"],
            reply_to=data["reply_to"],
            last_response=data,
            entry=entry,
        )
        new_comment.save()

        return Response()
