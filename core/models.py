from django.db import models

# Create your models here.

DIRECCION_SERVIDOR_LIBROS = 'file://172.20.30.114/'

class Descriptor(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre
    
class Empresa(models.Model):
    nombre = models.CharField(max_length=200, unique = True)

    def __str__(self):
        return self.nombre

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField('', null  = True, blank = True)
    autores = models.CharField('Autores de la publicación separados por ;', max_length=200, null  = True, blank = True)
    ano_publicacion = models.SmallIntegerField('Año de publicacion', null  = True, blank = True)
    archivo = models.FileField('Archivo', upload_to='libros/', max_length=200, null  = True, blank = True)
    descriptores = models.ManyToManyField(Descriptor, blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        abstract = True
        ordering = ('titulo','ano_publicacion')
    
class Libro(Publicacion):
    codigo = models.CharField(max_length=50, unique=True)
    cdinf = models.CharField("C. de Inf.", max_length=50, default="INDESCA")
    cdlc = models.CharField("Clasificación de LC", max_length=50)
    cdcuter = models.CharField("Código de Cuter", max_length=50, null=True, blank=True)
    cddewey = models.CharField("Código de Dewey", max_length=50, null=True, blank=True)

class Informe(Publicacion):
    no_registro = models.CharField(max_length=50, unique=True)
    programa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo_proyecto = models.CharField(max_length=50, null=True, blank=True)
    solicitud_servicio = models.CharField(max_length=20, null=True, blank=True)