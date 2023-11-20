from django.urls import path
from authentication.views import login_user, logout_user, GoogleLoginApi

urlpatterns = [
   path("google/", GoogleLoginApi.as_view(),
         name="login-with-google"),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
