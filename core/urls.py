from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('study/<str:pk>', views.study, name="study"), # Maybe we put this in the individual study
    path('login', views.blank_url, name="login"),
    path('logout', views.blank_url, name="logout"),
    path('update_user', views.blank_url, name="update-user")
]

