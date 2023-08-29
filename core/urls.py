from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('study/<str:pk>/', views.study, name="study"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('studies/weekday-studies/', include('weekdayStudy.urls')),
    path('auth/', include('users.urls'))
]

