from django.contrib import admin
from django.urls import path, include
from .views import CreateRequestView, DeclineRequestController, ListRequestsController, AcceptRequestController

urlpatterns = [
    path('create/', CreateRequestView.as_view(), name='create_request'),
    path('', ListRequestsController.as_view(), name='list_requests'),
    path('decline/<int:id>', DeclineRequestController.as_view(), name='decline_request'),
    path('accept/<int:id>', AcceptRequestController.as_view(), name='accept_request'),
]
