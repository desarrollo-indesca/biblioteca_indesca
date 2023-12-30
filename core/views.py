from django.shortcuts import render
from django.views.generic import ListView
from .models import Libro

# Create your views here.

class BusquedaLibros(ListView):
    template_name = 'busqueda_libros.html'
    context_object_name = 'libros'
    
    def get_queryset(self):
        return Libro.objects.all()
    
def filtrar_libros(request):
    autor = request.GET.get('autor', None)
    titulo = request.GET.get('titulo', None)
    descriptor = request.GET.get('descriptor', None)
    ano = request.GET.get('ano', None)

    libros = None

    if(autor):
        libros = Libro.objects.filter(autores__icontains=autor)

    if(titulo):
        libros = Libro.objects.filter(titulo__icontains=titulo) if not libros else libros.filter(titulo__icontains=titulo)

    if(ano):
        libros = Libro.objects.filter(ano_publicacion__icontains=ano) if not libros else libros.filter(ano_publicacion__icontains=ano)

    print(libros)

    if(not libros):
        libros = Libro.objects.all()

    return render(request, 'partials/lista_libros.html', {'libros': libros})