from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    #path('study/<str:pk>', views.study, name="study"), # Maybe we put this in the individual study
    path('studies/weekday-studies/', include('weekdayStudy.urls')),
]

