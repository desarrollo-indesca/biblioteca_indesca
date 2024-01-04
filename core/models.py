from django.db import models

# Create your models here.

class Descriptor(models.Model):
    '''
    Resumen:
        Modelo que representa un descriptor.

    Atributos:
        nombre: models.CharField -> Nombre del descriptor.
    
    Métodos:
        __str__(self): Retorna el nombre del descriptor.
    '''
    nombre = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.nombre
    
class Empresa(models.Model):
    '''
    Resumen:
        Modelo que representa una empresa para los programas de los informes.

    Atributos:
        nombre: models.CharField -> Nombre de la empresa.
    
    Métodos:
        __str__(self): Retorna el nombre de la empresa.
    '''
    nombre = models.CharField(max_length=200, unique = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        # Se ordena por nombre
        ordering = ('nombre',)

class Publicacion(models.Model):
    '''
    Resumen:
        Modelo abstracto que representa una publicación. Este es un modelo abstracto debido a que no se creará una tabla en la base de datos para este modelo, sino que se creará una tabla para cada modelo que herede de este.

    Atributos:
        titulo: models.CharField -> Título de la publicación.
        resumen: models.TextField -> Resumen de la publicación.
        autores: models.CharField -> Autores de la publicación.
        ano_publicacion: models.SmallIntegerField -> Año de publicación de la publicación.
        archivo: models.FileField -> Archivo de la publicación. Se guarda la dirección.
        descriptores: models.ManyToManyField -> Descriptores de la publicación.

    Métodos:
        __str__(self): Retorna el título de la publicación.
    '''
    titulo = models.CharField(max_length=500)
    resumen = models.TextField('', null  = True, blank = True)
    autores = models.CharField('Autores de la publicación separados por ;', max_length=200, null  = True, blank = True)
    ano_publicacion = models.SmallIntegerField('Año de publicacion', null  = True, blank = True)
    archivo = models.FileField('Archivo', upload_to='libros/', max_length=200, null  = True, blank = True)
    descriptores = models.ManyToManyField(Descriptor, blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        # Se ordena por título y año de publicación. Es una clase abstracta, por lo que no se creará una tabla en la base de datos para este modelo.
        abstract = True
        ordering = ('titulo','ano_publicacion')
    
class Libro(Publicacion):
    '''
    Resumen:
        Modelo que representa un libro.

    Hereda de:
        Publicacion: Debido a que un libro es una publicación.

    Atributos:
        codigo: models.CharField -> Código del libro.
        cdinf: models.CharField -> Código de información del libro.
        cdlc: models.CharField -> Código de LC del libro.
        cdcuter: models.CharField -> Código de cuter del libro.
        cddewey: models.CharField -> Código de Dewey del libro.

    Métodos:
        __str__(self): Retorna el código del libro.
    '''
    codigo = models.CharField(max_length=50, unique=True)
    cdinf = models.CharField("C. de Inf.", max_length=50, default="INDESCA")
    cdlc = models.CharField("Clasificación de LC", max_length=50)
    cdcuter = models.CharField("Código de Cuter", max_length=200, null=True, blank=True)
    cddewey = models.CharField("Código de Dewey", max_length=50, null=True, blank=True)

class Informe(Publicacion):
    '''
    Resumen:
        Modelo que representa un informe técnico de Indesca.

    Hereda de:
        Publicacion: Debido a que un informe es una publicación.

    Atributos:
        archivo: models.FileField -> Archivo del informe. Se guarda en dirección dinámica.
        no_registro: models.CharField -> Número de registro del informe.
        programa: models.ForeignKey -> Programa al que pertenece el informe.
        codigo_proyecto: models.CharField -> Código del proyecto del informe.
        solicitud_servicio: models.CharField -> Solicitud de servicio del informe.

    Métodos:
        __str__(self): Retorna el número de registro del informe.
        upload_to(self, filename): Retorna la dirección donde se guardará el archivo del informe.    
    '''
    def upload_to(self, filename):
        return f'informes/{self.programa}/{self.ano_publicacion}/{filename}'
    
    archivo = models.FileField('Archivo', upload_to=upload_to, max_length=200, null  = True)
    no_registro = models.CharField(max_length=50, unique=True)
    programa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo_proyecto = models.CharField(max_length=50, null=True, blank=True)
    solicitud_servicio = models.CharField(max_length=50, null=True, blank=True)