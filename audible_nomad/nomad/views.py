from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import random
import json
import requests

from lsh_model.predict import predict_book_and_location

BOOKS_MAP = {
    'robot_of_dawn-final':'B00KTEH7WQ',
    'ready_player_one-final': 'B005FRGT44'}

# def predict_book_and_location(list_of_words):
#     return random.choice(BOOKS_MAP.keys()), 0.0


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
        title, ms_start = predict_book_and_location(list_of_words)

        # api call to get product details from ASIN
        try:
            asin = BOOKS_MAP[title]
        except KeyError:
            # emergency valve
            asin = 'B005FRGT44'

        return Response({'ASIN': asin,
                         'start_milliseconds': ms_start})
