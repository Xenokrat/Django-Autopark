from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    path("", HttpResponse("<h1>Hello World!</h1>")),
]
