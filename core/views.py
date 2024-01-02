from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import Libro
from .forms import LibroForm

# Create your views here.

class BusquedaLibros(ListView):
    context_object_name = 'libros'
    paginate_by = 20

    def get_template_names(self) -> list:
        if(self.request.htmx):
            return 'partials/lista_libros.html'
        
        return 'busqueda_libros.html'
    
    def filtro_libros(self):
        autor = self.request.GET.get('autor', None)
        titulo = self.request.GET.get('titulo', None)
        descriptores = self.request.GET.get('descriptores', None)
        ano = self.request.GET.get('ano', None)

        libros, prev_libros = None, None

        if(autor):
            libros = Libro.objects.filter(autores__icontains=autor)
            prev_libros = libros

        if(titulo):
            libros = Libro.objects.filter(titulo__icontains=titulo) if not libros else libros.filter(titulo__icontains=titulo)
        
        if(libros):
            prev_libros = libros
        else:
            libros = prev_libros

        if(ano):
            libros = Libro.objects.filter(ano_publicacion__icontains=ano) if not libros else libros.filter(ano_publicacion__icontains=ano)

        if(libros):
            prev_libros = libros
        else:
            libros = prev_libros

        if(descriptores):
            for descriptor in descriptores.split(';'):
                descriptor = descriptor.strip()
                libros = Libro.objects.filter(descriptores__nombre__icontains=descriptor) if not libros else libros.filter(descriptores__nombre__icontains=descriptor)

        if(not libros):
            libros = prev_libros
        else:
            libros = libros.distinct()

        return libros
    
    def get_queryset(self):
        libros = None

        if(self.request.htmx and len(self.request.GET.keys())):
            libros = self.filtro_libros()
        
        if((not self.request.htmx or self.request.GET.get('page',None)) and not libros ):
            libros = Libro.objects.all()

        if(libros):
            libros.prefetch_related('descriptores')

        return libros

class CreacionLibro(CreateView):
    template_name = 'libro_form.html'
    form_class = LibroForm
    success_url = '/'

class EdicionLibro(UpdateView):
    template_name = 'libro_form.html'
    form_class = LibroForm
    success_url = '/'
    model = Libro

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de Libro'
        context['form'].fields['descriptores'].initial = "; ".join(context['object'].descriptores.all().order_by('nombre').values_list('nombre', flat=True))

        return context

def obtener_libro(request, pk):
    libro = Libro.objects.get(pk=pk)

    pass