from django.urls import path
from .views import *

urlpatterns = [
    path('busqueda/libros/', BusquedaLibros.as_view(), name='busqueda_libros'),
    path('creacion/libro/', CreacionLibro.as_view(), name='creacion_libro'),
    path('edicion/libro/<int:pk>/', EdicionLibro.as_view(), name='edicion_libro'),
    path('eliminacion/libro/<int:pk>/', eliminar_libro, name='eliminacion_libro'),
    path('busqueda/informes/', BusquedaInformes.as_view(), name='busqueda_informes'),

]
