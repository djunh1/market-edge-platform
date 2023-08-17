from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('study/', views.study, name="study"),
    path('login', views.blank_url, name="login"),
    path('logout', views.blank_url, name="logout"),
    path('update_user', views.blank_url, name="update-user")
]

