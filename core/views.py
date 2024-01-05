from typing import Any
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse
from .models import Libro, Informe
from .forms import LibroForm, InformeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from usuarios.views import SuperUserRequiredMixin

# Create your views here.
class BusquedaLibros(ListView):
    '''
    Resumen:
        Vista que permite la búsqueda de libros.

    Hereda de:
        ListView: Debido a que se mostrará una lista de libros.

    Atributos:
        context_object_name: str -> Nombre del objeto que se pasará al template.
        paginate_by: int -> Número de elementos por página.

    Métodos:
        get_context_data(self, **kwargs): Retorna el contexto de la vista.
        get_template_names(self): Retorna el nombre del template que se usará.
        filtro_libros(self, modelo): Retorna los libros filtrados según los parámetros de búsqueda.
        get_queryset(self): Retorna los libros que se mostrarán en la lista.
    '''
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

        # Si se está usando htmx y se están enviando parámetros de búsqueda (Filtrado)
        if(self.request.htmx and len(self.request.GET.keys())):
            libros = self.filtro_libros()

            if(not libros and len(self.request.GET.keys())):
                libros = Libro.objects.none()
        
        # Si no se está usando htmx y no se están enviando parámetros de búsqueda (Listado/Paginación)
        if((not self.request.htmx or all(y == '' for x,y in self.request.GET.items() if x != 'page' )) and not libros):
            libros = Libro.objects.all()

        # Para mejorar la eficiencia
        if(libros):
            libros.prefetch_related('descriptores')

        return libros

class CreacionLibro(SuperUserRequiredMixin, CreateView):
    '''
    Resumen:
        Vista que permite la creación de un libro.

    Hereda de:
        CreateView: Debido a que se creará un libro.
    
    Implementa:
        SuperUserRequiredMixin: Debido a que solo los superusuarios pueden crear libros.

    Atributos:
        template_name: str -> Nombre del template que se usará.
        form_class: forms.ModelForm -> Formulario que se usará.
        success_url: str -> URL a la que se redirigirá al crear el libro.

    Métodos:
        get_context_data(self, **kwargs): Retorna el contexto de la vista.
    '''
    template_name = 'libro_form.html'
    form_class = LibroForm
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict:
        return {'titulo': 'Registro de Nuevo Libro', **super().get_context_data(**kwargs)}

class EdicionLibro(SuperUserRequiredMixin, UpdateView):
    '''
    Resumen:
        Vista que permite la edición de un libro.

    Hereda de:
        UpdateView: Debido a que se editará un libro.

    Implementa:
        SuperUserRequiredMixin: Debido a que solo los superusuarios pueden editar libros.

    Atributos:
        template_name: str -> Nombre del template que se usará.
        form_class: forms.ModelForm -> Formulario que se usará.
        success_url: str -> URL a la que se redirigirá al editar el libro.
        model: models.Libro -> Modelo que se usará.
    '''
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
    '''
    Resumen:
        Elimina un libro.

    Argumentos:
        request: HttpRequest -> Solicitud HTTP.
        pk: int -> ID del libro a eliminar.

    Retorna:
        HttpResponse -> Respuesta HTTP. Estatus 200 si fue exitoso, 403 si no.
    '''
    if(request.method == 'POST' and request.user.is_superuser):
        libro = Libro.objects.get(id=pk)
        libro.delete()

        return HttpResponse(status=200)
    
    return HttpResponse(status=403)

class BusquedaInformes(LoginRequiredMixin, BusquedaLibros):
    '''
    Resumen:
        Vista que permite la búsqueda de informes.

    Hereda de:
        BusquedaLibros: Debido a que se mostrará una lista de informes.

    Implementa:
        LoginRequiredMixin: Debido a que solo los usuarios logueados pueden buscar informes.

    Atributos:
        context_object_name: str -> Nombre del objeto que se pasará al template.
        paginate_by: int -> Número de elementos por página.

    Métodos:
        get_context_data(self, **kwargs): Retorna el contexto de la vista.
        get_template_names(self): Retorna el nombre del template que se usará dependiendo de si se utiliza HTMX o no.
        filtro_libros(self, modelo): Retorna los informes filtrados según los parámetros de búsqueda.
        get_queryset(self): Retorna los informes que se mostrarán en la lista.
    '''
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
    '''
    Resumen:
        Vista que permite la creación de un informe.

    Hereda de:
        CreateView: Debido a que se creará un informe.

    Implementa:
        SuperUserRequiredMixin: Debido a que solo los superusuarios pueden crear informes.

    Atributos:
        template_name: str -> Nombre del template que se usará.
        form_class: forms.ModelForm -> Formulario que se usará.
        success_url: str -> URL a la que se redirigirá al crear el informe.

    Métodos:
        get_context_data(self, **kwargs): Retorna el contexto de la vista.
    '''
    template_name = 'informe_form.html'
    form_class = InformeForm
    success_url = 'publicaciones/busqueda/informes/'

    def get_context_data(self, **kwargs: Any) -> dict:
        return {'titulo': 'Registro de Informe Técnico', **super().get_context_data(**kwargs)}

class EdicionInforme(SuperUserRequiredMixin, UpdateView):
    '''
    Resumen:
        Vista que permite la edición de un informe.

    Hereda de:
        UpdateView: Debido a que se editará un informe.

    Implementa:
        SuperUserRequiredMixin: Debido a que solo los superusuarios pueden editar informes.

    Atributos:
        template_name: str -> Nombre del template que se usará.
        form_class: forms.ModelForm -> Formulario que se usará.
        success_url: str -> URL a la que se redirigirá al editar el informe.
        model: models.Informe -> Modelo que se usará.

    Métodos:
        get_context_data(self, **kwargs): Retorna el contexto de la vista. Realiza manualmente la construcción del valor inicial del campo "descriptores".
    '''
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
    '''
    Resumen:
        Elimina un informe según su PK. Únicamente si el usuario es superusuario.

    Argumentos:
        request: HttpRequest -> Solicitud HTTP.
        pk: int -> ID del informe a eliminar.

    Retorna:
        HttpResponse -> Respuesta HTTP. Estatus 200 si fue exitoso, 403 si no.
    '''
    if(request.method == 'POST' and request.user.is_superuser):
        informe = Informe.objects.get(id=pk)
        informe.delete()
        return HttpResponse(status=200)
    
    return HttpResponse(status=403)
