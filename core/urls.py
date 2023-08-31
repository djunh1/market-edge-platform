from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('main/', views.home, name="home"),
    path('study/<str:pk>/', views.study, name="study"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"), #Will prob delete
    path('studies/weekday-studies/', include('weekdayStudy.urls')),
    
    path('auth/', include('users.urls'))
]

