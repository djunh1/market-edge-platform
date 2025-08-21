from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


from django.http import HttpResponse



urlpatterns = [
    path("admin/", admin.site.urls),
    path('portfolios/', include('portfolios.urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('api.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)