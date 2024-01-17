from typing import Any
from django.forms.models import BaseModelForm
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse
from .models import Libro, Informe
from .forms import LibroForm, InformeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from usuarios.views import SuperUserRequiredMixin
from django.urls import reverse

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
        autor = self.request.GET.get('autor', None) if self.request.GET.get('autor', None) and self.request.GET.get('autor', None) not in ['','None'] else None
        titulo = self.request.GET.get('titulo', None) if self.request.GET.get('titulo', None) and self.request.GET.get('titulo', None) not in ['','None'] else None
        descriptores = self.request.GET.get('descriptores', None) if self.request.GET.get('descriptores', None) and self.request.GET.get('descriptores', None) not in ['','None'] else None
        ano = self.request.GET.get('ano', None) if self.request.GET.get('ano', None) and self.request.GET.get('ano', None) not in ['','None'] else None
        archivo = int(self.request.GET.get('archivo', 0)) if self.request.GET.get('archivo', None) and self.request.GET.get('archivo') not in ['', 'None'] else None

        # Aquí el session se utiliza para guardar los parámetros de búsqueda para que se mantengan al cambiar de página
        if(not self.request.htmx):
            if(not autor and (self.request.session.get('params_libros') or self.request.session.get('params_informes'))):
                if(modelo == Libro):
                    autor = self.request.session.get('params_libros').get('autor') if self.request.session.get('params_libros') and self.request.session['params_libros']['autor'] not in ['', 'None'] else None
                elif(modelo == Informe):
                    autor = self.request.session.get('params_informes').get('autor') if self.request.session.get('params_informes') and self.request.session['params_informes']['autor'] not in ['', 'None'] else None

            if(not titulo and (self.request.session.get('params_libros') or self.request.session.get('params_informes'))):
                if(modelo == Libro):
                    titulo = self.request.session.get('params_libros').get('titulo') if self.request.session.get('params_libros') and self.request.session['params_libros']['titulo'] not in ['', 'None'] else None
                elif(modelo == Informe):
                    titulo = self.request.session.get('params_informes').get('titulo') if self.request.session.get('params_informes') and self.request.session['params_informes']['titulo'] not in ['', 'None'] else None

            if(not descriptores and (self.request.session.get('params_libros') or self.request.session.get('params_informes'))):
                if(modelo == Libro):
                    descriptores = self.request.session.get('params_libros').get('descriptores') if self.request.session.get('params_libros') and self.request.session['params_libros']['descriptores'] not in ['', 'None'] else None
                elif(modelo == Informe):
                    descriptores = self.request.session.get('params_informes').get('descriptores') if self.request.session.get('params_informes') and self.request.session['params_informes']['descriptores'] not in ['', 'None'] else None

            if(not ano and (self.request.session.get('params_libros') or self.request.session.get('params_informes'))):
                if(modelo == Libro):
                    ano = self.request.session.get('params_libros').get('ano') if self.request.session.get('params_libros') and self.request.session['params_libros']['ano'] not in ['', 'None'] else None
                elif(modelo == Informe):
                    ano = self.request.session.get('params_informes').get('ano') if self.request.session.get('params_informes') and self.request.session['params_informes']['ano'] not in ['', 'None'] else None

            if(not archivo and (self.request.session.get('params_libros') or self.request.session.get('params_informes'))):
                if(modelo == Libro):
                    archivo = self.request.session.get('params_libros').get('archivo') if self.request.session.get('params_libros') and self.request.session['params_libros']['archivo'] not in ['', 'None'] else None
                elif(modelo == Informe):
                    archivo = self.request.session.get('params_informes').get('archivo') if self.request.session.get('params_informes') and self.request.session['params_informes']['archivo'] not in ['', 'None'] else None

        libros = None

        if(autor):
            libros = modelo.objects.filter(autores__icontains=autor)
        
        if(titulo):
            libros = modelo.objects.filter(titulo__icontains=titulo) if libros == None else libros.filter(titulo__icontains=titulo)

        if(ano):
            libros = modelo.objects.filter(ano_publicacion__icontains=ano) if libros == None else libros.filter(ano_publicacion__icontains=ano)

        if(descriptores):
            for descriptor in descriptores.split(';'):
                descriptor = descriptor.strip()
                libros = modelo.objects.filter(descriptores__nombre__icontains=descriptor) if libros == None else libros.filter(descriptores__nombre__icontains=descriptor)

        if(libros):
            libros = libros.distinct()

        if(archivo):
            libros_sin_dir = [x.pk for x in libros if x.archivo_existe()] if libros else [x.pk for x in modelo.objects.all() if x.archivo_existe()]
            libros = modelo.objects.filter(pk__in=libros_sin_dir) if libros == None else libros.filter(pk__in=libros_sin_dir)
        elif(archivo == 0):
            libros_sin_dir = [x.pk for x in libros if not x.archivo_existe()] if libros else [x.pk for x in modelo.objects.all() if not x.archivo_existe()]
            libros = modelo.objects.filter(pk__in=libros_sin_dir) if libros == None else libros.filter(pk__in=libros_sin_dir)

        # Si se está usando htmx y se están enviando parámetros de búsqueda (Filtrado), se guardarán los mismos para que se mantengan al volver a la página
        if(self.request.htmx):
            if(modelo == Libro):
                self.request.session['params_libros'] = {}
                self.request.session['params_libros']['autor'] = autor
                self.request.session['params_libros']['titulo'] = titulo
                self.request.session['params_libros']['descriptores'] = descriptores
                self.request.session['params_libros']['ano'] = ano
                self.request.session['params_libros']['archivo'] = archivo
            elif(modelo == Informe):
                self.request.session['params_informes'] = {}
                self.request.session['params_informes']['autor'] = autor
                self.request.session['params_informes']['titulo'] = titulo
                self.request.session['params_informes']['descriptores'] = descriptores
                self.request.session['params_informes']['ano'] = ano
                self.request.session['params_informes']['archivo'] = archivo
       
        return libros
    
    def get_queryset(self):
        libros = None

        # Filtrar libros de acuerdo a los parámetros de búsqueda
        libros = self.filtro_libros()
        
        # Si no se está usando htmx y no se están enviando parámetros de búsqueda (Listado/Paginación)
        if((all(y == '' for x,y in self.request.GET.items() if x != 'page') or not self.request.htmx) and (not libros or not libros.count())):
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
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Búsqueda de Informes Técnicos'
        return context
    
    def filtro_libros(self, modelo = Informe):
        informes = super().filtro_libros(modelo)

        solicitud_servicio = self.request.GET.get('solicitud_servicio', None)
        programa = self.request.GET.get('programa', None)

        print(informes)

        if(not self.request.htmx):
            if(not solicitud_servicio and self.request.session.get('params_informes')):
                solicitud_servicio = self.request.session['params_informes']['solicitud_servicio'] if self.request.session.get('params_informes') and self.request.session['params_informes']['solicitud_servicio'] not in ['', 'None'] else None
            
            if(not programa and self.request.session.get('params_informes')):
                programa = self.request.session['params_informes']['programa'] if self.request.session.get('params_informes') and self.request.session['params_informes']['programa'] not in ['', 'None'] else None

        if(solicitud_servicio):
            informes = modelo.objects.filter(solicitud_servicio__icontains=solicitud_servicio) if informes == None else informes.filter(solicitud_servicio__icontains=solicitud_servicio)

        if(programa):
           informes = modelo.objects.filter(programa__nombre__icontains=programa) if informes == None else informes.filter(programa__nombre__icontains=programa)

        if(self.request.htmx):
            self.request.session['params_informes']['solicitud_servicio'] = solicitud_servicio
            self.request.session['params_informes']['programa'] = programa

        return informes
    
    def get_queryset(self):
        informes = None

        informes = self.filtro_libros()

        if(not informes and len(self.request.GET.keys())):
            informes = Informe.objects.none()
        
        if((not self.request.htmx or all(y == '' for x,y in self.request.GET.items() if x != 'page')) and (not informes or not informes.count())):
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
    success_url = '/publicaciones/busqueda/informes/'

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

def obtener_archivo_libro(request, pk):
    '''
    Resumen:
        Obtiene el archivo de un libro según su PK.

    Argumentos:
        request: HttpRequest -> Solicitud HTTP.
        pk: int -> ID del libro del que se quiere obtener el archivo.

    Retorna:
        HttpResponse -> Respuesta HTTP. Estatus 200 si fue exitoso, 403 o 404 si no.
    '''
    try:
        if(request.method == 'GET'):
            libro = Libro.objects.get(id=pk)
            if(libro.archivo_existe()):
                with open(libro.archivo.path, 'rb') as f:
                    if(libro.archivo.name.lower().endswith('.pdf')):
                        response = HttpResponse(f.read(), content_type='application/pdf')
                    else:
                        response = HttpResponse(f.read())
                        response['Content-Disposition'] = 'attachment; filename=' + libro.archivo.name
                return response
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)
    except:
        return HttpResponse(status=404)
    
def obtener_archivo_informe(request, pk):
    '''
    Resumen:
        Obtiene el archivo de un informe según su PK.

    Argumentos:
        request: HttpRequest -> Solicitud HTTP.
        pk: int -> ID del informe del que se quiere obtener el archivo.

    Retorna:
        HttpResponse -> Respuesta HTTP. Estatus 200 si fue exitoso, 403 o 404 si no.
    '''
    try:
        if(request.method == 'GET' and request.user.is_authenticated):
            informe = Informe.objects.get(id=pk)
            if(informe.archivo_existe()):
                with open(informe.archivo.path, 'rb') as f:
                    print(informe.archivo.name)
                    if(informe.archivo.name.lower().endswith('.pdf')):
                        response = HttpResponse(f.read(), content_type='application/pdf')
                    else:
                        response = HttpResponse(f.read())
                        response['Content-Disposition'] = 'attachment; filename=' + informe.archivo.name
                return response
            else:
                return HttpResponse(status=404)
        elif(not request.user.is_authenticated):
            return HttpResponse(status=403)
    except:
        return HttpResponse(status=404)