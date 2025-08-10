from django.contrib import admin
from .models import Portfolio, Tag, Review

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Tag)
admin.site.register(Review)