from django.urls import path
from .views import *

urlpatterns = [
    path('busqueda/libros/', BusquedaLibros.as_view(), name='busqueda_libros'),
    path('creacion/libro/', CreacionLibro.as_view(), name='creacion_libro'),
    path('obtener/libro/<int:pk>/',obtener_libro, name='obtener_libro'),
]
