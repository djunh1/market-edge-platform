from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="register"),
    path('update-user/', views.updateUser, name="update-user"),
    ]
