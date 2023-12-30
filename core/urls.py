from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('/busqueda/libros/', BusquedaLibros.as_view(), name='busqueda_libros'),
]
