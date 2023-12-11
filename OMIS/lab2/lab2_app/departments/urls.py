from django.contrib import admin
from django.urls import path, include
from .views import AvailableObjectsController, EnterDepartmentController, ExitDepartmentController

urlpatterns = [
    path('', AvailableObjectsController.as_view(), name='get_available_objects'),
    path('enter/<int:id>', EnterDepartmentController.as_view(), name='enter_department'),
    path('exit/', ExitDepartmentController.as_view(), name='exit_department'),
]
