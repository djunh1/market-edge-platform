from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('create-weekday-study/', views.createWeekdayStudy, name="create-weekday-study"),
    path('weekday-study/<str:pk>', views.study, name="weekday-study"),
]
