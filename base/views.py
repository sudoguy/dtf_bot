from rest_framework.response import Response
from rest_framework.views import APIView

from base.tasks import handle_comment


class NewComment(APIView):
    def post(self, request):
        data = request.data["data"]

        handle_comment.delay(data)

        return Response()
