from django import forms
from .models import Libro, Descriptor, Informe
from django.db import transaction 

class GuardadoDescriptoresMixin(forms.ModelForm):
    descriptores = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Separe cada descriptor con el carácter ";"'}))

    def save(self, commit: bool = ...):
        res = super().save(commit)
        
        if(commit):
            with transaction.atomic():
                descriptores = self.cleaned_data['descriptores'].split(';')
                
                if(self.instance.pk):
                    self.instance.descriptores.clear()

                for descriptor in descriptores:
                    descriptor = descriptor.strip().upper()
                    if(descriptor == '' or descriptor == 'NONE'):
                        continue
                    descriptor = Descriptor.objects.get_or_create(nombre=descriptor)[0]

                    if(not res.descriptores.filter(nombre=descriptor.nombre).exists()):
                        res.descriptores.add(descriptor)

        return res

class LibroForm(GuardadoDescriptoresMixin):
    '''
    Resumen:
        Formulario para la creación de un libro.

    Hereda de:
        GuardadoDescriptoresMixin: Debido a que se reutilizará el método save() de GuardadoDescriptoresMixin.

    Atributos:
        descriptores: forms.CharField -> Campo de texto para ingresar los descriptores del libro.
    '''
    
    class Meta:
        model = Libro
        exclude = ['id', 'descriptores']

class InformeForm(GuardadoDescriptoresMixin):
    '''
    Resumen:
        Formulario para la creación de un informe.

    Hereda de:
        LibroForm: Debido a que se reutilizará la función save() de LibroForm.

    Atributos:
        descriptores: forms.CharField -> Campo de texto para ingresar los descriptores del informe.

    Métodos:
        save(self, commit): Guarda el informe y los descriptores ingresados. El parámetro "commit" indica si se debe guardar el informe en la base de datos.
    '''

    class Meta:
        model = Informe
        exclude = ['id', 'descriptores']