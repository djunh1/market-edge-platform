from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('update-user/', views.updateUser, name="update-user"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    ]
