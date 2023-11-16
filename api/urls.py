'''Contains the URL patterns for the API app.'''
from django.urls import path

from .views import UserAPI
from .views import AuthAPI


urlpatterns = [
    path('user/', UserAPI.as_view(), name='User'),
    path('auth/', AuthAPI.as_view(), name='Auth'),
]