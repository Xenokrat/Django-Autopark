from django.http import HttpResponse
from django.urls import path

from .views import index

urlpatterns = [
    path("", index),
]
