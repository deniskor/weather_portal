from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('', home_page, name='home'),
    path('', home_page, name='home_page'),
    path('get_city/', get_city, name='get_city'),
]
