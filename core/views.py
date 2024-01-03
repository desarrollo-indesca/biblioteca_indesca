from typing import Any
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse
from .models import Libro, Informe
from .forms import LibroForm, InformeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from usuarios.views import SuperUserRequiredMixin

# Create your views here.
class BusquedaLibros(ListView):
    context_object_name = 'libros'
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict:
        return {'titulo': 'Búsqueda de Libros', **super().get_context_data(**kwargs)}
    
    def get_template_names(self) -> list:
        if(self.request.htmx):
            return 'partials/lista_libros.html'
        
        return 'busqueda_libros.html'
    
    def filtro_libros(self, modelo = Libro):
        autor = self.request.GET.get('autor', None)
        titulo = self.request.GET.get('titulo', None)
        descriptores = self.request.GET.get('descriptores', None)
        ano = self.request.GET.get('ano', None)

        libros, prev_libros = None, None

        if(autor):
            libros = modelo.objects.filter(autores__icontains=autor)
            prev_libros = libros

        if(titulo):
            libros = modelo.objects.filter(titulo__icontains=titulo) if not libros else libros.filter(titulo__icontains=titulo)
        
        if(libros):
            prev_libros = libros
        else:
            libros = prev_libros

        if(ano):
            libros = modelo.objects.filter(ano_publicacion__icontains=ano) if not libros else libros.filter(ano_publicacion__icontains=ano)

        if(libros):
            prev_libros = libros
        else:
            libros = prev_libros

        if(descriptores):
            for descriptor in descriptores.split(';'):
                descriptor = descriptor.strip()
                libros = modelo.objects.filter(descriptores__nombre__icontains=descriptor) if not libros else libros.filter(descriptores__nombre__icontains=descriptor)

        if(not libros):
            libros = prev_libros
        else:
            libros = libros.distinct()

        return libros
    
    def get_queryset(self):
        libros = None

        if(self.request.htmx and len(self.request.GET.keys())):
            libros = self.filtro_libros()

            if(not libros and len(self.request.GET.keys())):
                libros = Libro.objects.none()
        
        if((not self.request.htmx or all(y == '' for x,y in self.request.GET.items() if x != 'page' )) and not libros):
            libros = Libro.objects.all()

        if(libros):
            libros.prefetch_related('descriptores')

        return libros

class CreacionLibro(SuperUserRequiredMixin, CreateView):
    template_name = 'libro_form.html'
    form_class = LibroForm
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict:
        return {'titulo': 'Registro de Nuevo Libro', **super().get_context_data(**kwargs)}

class EdicionLibro(SuperUserRequiredMixin, UpdateView):
    template_name = 'libro_form.html'
    form_class = LibroForm
    success_url = '/'
    model = Libro

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de Libro'
        context['form'].fields['descriptores'].initial = "; ".join(context['object'].descriptores.all().order_by('nombre').values_list('nombre', flat=True))

        return context
    
def eliminar_libro(request, pk):
    if(request.method == 'POST' and request.user.is_superuser):
        libro = Libro.objects.get(id=pk)
        libro.delete()

        return HttpResponse(status=200)
    
    return HttpResponse(status=402)

class BusquedaInformes(LoginRequiredMixin, BusquedaLibros):
    context_object_name = 'informes'
    paginate_by = 20

    def get_template_names(self) -> list:
        if(self.request.htmx):
            return 'partials/lista_informes.html'
        
        return 'busqueda_informes.html'
    
    def get_context_data(self, **kwargs: Any) -> dict:
        return {'titulo': 'Búsqueda de Informes Técnicos', **super().get_context_data(**kwargs)}
    
    def filtro_libros(self, modelo = Informe):
        informes = super().filtro_libros(modelo)

        solicitud_servicio = self.request.GET.get('solicitud_servicio', None)
        programa = self.request.GET.get('programa', None)

        prev_informes = informes
        if(solicitud_servicio):
            informes = modelo.objects.filter(solicitud_servicio__icontains=solicitud_servicio) if not informes else informes.filter(solicitud_servicio__icontains=solicitud_servicio)

        if(not informes):
            informes = prev_informes

        if(programa):
            informes = modelo.objects.filter(programa__nombre__icontains=programa) if not informes else informes.filter(programa__nombre__icontains=programa)

        if(not informes):
            informes = prev_informes

        return informes
    
    def get_queryset(self):
        informes = None

        if(self.request.htmx and len(self.request.GET.keys())):
            informes = self.filtro_libros()

            if(not informes and len(self.request.GET.keys())):
                informes = Informe.objects.none()
        
        if((not self.request.htmx or all(y == '' for x,y in self.request.GET.items() if x != 'page')) and not informes):
            informes = Informe.objects.all()

        if(informes):
            informes.prefetch_related('descriptores')

        return informes

class CreacionInforme(SuperUserRequiredMixin, CreateView):
    template_name = 'informe_form.html'
    form_class = InformeForm
    success_url = 'publicaciones/busqueda/informes/'

    def get_context_data(self, **kwargs: Any) -> dict:
        return {'titulo': 'Registro de Informe Técnico', **super().get_context_data(**kwargs)}

class EdicionInforme(SuperUserRequiredMixin, UpdateView):
    template_name = 'informe_form.html'
    form_class = InformeForm
    success_url = '/publicaciones/busqueda/informes/'
    model = Informe

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de Informe Técnico'
        context['form'].fields['descriptores'].initial = "; ".join(context['object'].descriptores.all().order_by('nombre').values_list('nombre', flat=True))

        return context
    
def eliminar_informe(request, pk):
    if(request.method == 'POST' and request.user.is_superuser):
        informe = Informe.objects.get(id=pk)
        informe.delete()
        return HttpResponse(status=200)
    
    return HttpResponse(status=402)
