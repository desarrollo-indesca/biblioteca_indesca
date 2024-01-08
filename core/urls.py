from django.urls import path
from .views import *

urlpatterns = [
    path('busqueda/libros/', BusquedaLibros.as_view(), name='busqueda_libros'),
    path('creacion/libro/', CreacionLibro.as_view(), name='creacion_libro'),
    path('edicion/libro/<int:pk>/', EdicionLibro.as_view(), name='edicion_libro'),
    path('eliminacion/libro/<int:pk>/', eliminar_libro, name='eliminacion_libro'),

    path('busqueda/informes/', BusquedaInformes.as_view(), name='busqueda_informes'),
    path('creacion/informe/', CreacionInforme.as_view(), name='creacion_informe'),
    path('edicion/informe/<int:pk>/', EdicionInforme.as_view(), name='edicion_informe'),
    path('eliminacion/informe/<int:pk>/', eliminar_informe, name='eliminacion_informe'),

    path('lectura/libro/<int:pk>/', obtener_archivo_libro, name='leer_libro'),
    path('lectura/informe/<int:pk>/', obtener_archivo_informe, name='leer_informe'),
]
