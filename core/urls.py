from django.contrib import admin
from django.urls import path
from .views import bienvenida

urlpatterns = [
    path('', bienvenida, name='bienvenida'),
]
