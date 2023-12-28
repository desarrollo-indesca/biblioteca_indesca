from django.shortcuts import render
from django.views.generic import ListView
from .models import Libro

# Create your views here.

class BusquedaLibros(ListView):
    template_name = 'busqueda_libros.html'
    context_object_name = 'libros'
    
    def get_queryset(self):
        return Libro.objects.all()