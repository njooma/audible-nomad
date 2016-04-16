from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import json

# Create your views here.
class TextToBook(APIView):
    """
    Post  text to receive the book title
    """

    def post(self, request):
        text = json.loads(request.data.get("text"))
        for line in text:
            for word in line:
                # TODO: Plug into the function
                print word
        return Response()
