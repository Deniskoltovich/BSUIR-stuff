from django.contrib import admin
from django.urls import path, include
from .views import RegistrationController, DisplayUserController, EmployeeProfileController, ChangeUserGroupController, ChangeAccessForUserController, LogoutUserView, ChangePasswordController
urlpatterns = [
    path('register/', RegistrationController.as_view(), name='register'),
    path('login/', include('django.contrib.auth.urls')),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('', DisplayUserController.as_view(), name='list_users'),
    path('change_password', ChangePasswordController.as_view(), name='change_password'),
    path('create_employee/', EmployeeProfileController.as_view(), name='create_employee'),
    path('group/change/', ChangeUserGroupController.as_view(), name='change_user_group'),
    path('activity/<int:id>', DisplayUserController.as_view(), name = 'get_user_activities'),
    path('change/', ChangeAccessForUserController.as_view(), name='change_access_for_user'),

]
