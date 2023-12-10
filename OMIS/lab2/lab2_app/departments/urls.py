from django.contrib import admin
from django.urls import path, include
from .views import get_available_objects, enter_department, exit_department

urlpatterns = [
    path('', get_available_objects, name='get_available_objects'),
    path('enter/<int:id>', enter_department, name='enter_department'),
    path('exit/', exit_department, name='exit_department'),
]
