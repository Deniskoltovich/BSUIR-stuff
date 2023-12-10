from django.contrib import admin
from django.urls import path, include
from .views import create_request, decline_request, list_requests, accept_request

urlpatterns = [
    path('create/', create_request, name='create_request'),
    path('', list_requests, name='list_requests'),
    path('decline/<int:id>', decline_request, name='decline_request'),
    path('accept/<int:id>', accept_request, name='accept_request'),
]
