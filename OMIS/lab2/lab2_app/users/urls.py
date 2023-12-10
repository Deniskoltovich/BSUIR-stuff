from django.contrib import admin
from django.urls import path, include
from .views import register, list_users, create_employee, change_user_group, get_user_activities, change_access_for_user, logout_user, change_password
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('', list_users, name='list_users'),
    path('change_password', change_password, name='change_password'),
    path('create_employee/', create_employee, name='create_employee'),
    path('group/change/', change_user_group, name='change_user_group'),
    path('activity/<int:id>', get_user_activities, name = 'get_user_activities'),
    path('change/', change_access_for_user, name='change_access_for_user'),

]
