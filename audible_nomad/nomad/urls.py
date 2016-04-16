from __future__ import absolute_import

from django.conf.urls import url, include

from .views import TextToBook

# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^text-to-book/', TextToBook.as_view(), name="TextToBook"),
]