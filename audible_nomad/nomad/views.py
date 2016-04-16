from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import json

def marks_function(list_of_words):
    ASIN = 'xxxx'
    return ASIN

# Create your views here.
class TextToBook(APIView):
    """
    Post  text to receive the book title
    """

    def post(self, request):

        text = request.data.get("text", [])
        list_of_words = []
        for inner_list in text:
            list_of_words.extend(inner_list)
        print list_of_words

        # mark to get right book
        asin_code = marks_function(list_of_words)

        # api call to get product details from ASIN


        return Response({'ASIN': asin_code})
