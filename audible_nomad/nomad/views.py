from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import random
import json
import requests

BOOKS_MAP = {
    'innovators-final': 'B00M9KA2ZM',
    'Martian':'B00B5HO5XA',
    'Beautiful-and-the-Damned': 'B00847O20A',
    'robot_of_dawn-final':'B0024NP57Y',
    'ready_player_one-final': 'B005CVWWJY'}

def marks_function(list_of_words):
    return random.choice(BOOKS_MAP.keys())


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
        title = marks_function(list_of_words)

        # api call to get product details from ASIN

        return Response({'ASIN': BOOKS_MAP[title]})
