from django import forms
from .models import Libro, Descriptor, Informe

class LibroForm(forms.ModelForm):
    descriptores = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Separe cada descriptor con el carácter ";"'}))

    def save(self, commit: bool = ...):
        res = super().save(commit)
        
        if(commit):
            descriptores = self.cleaned_data['descriptores'].split(';')
            print(descriptores)
            for descriptor in descriptores:
                descriptor = descriptor.strip().upper()
                print(descriptor)
                if(descriptor == '' or descriptor == 'NONE'):
                    continue
                descriptor = Descriptor.objects.get_or_create(nombre=descriptor)[0]

                if(not res.descriptores.filter(nombre=descriptor.nombre).exists()):
                    res.descriptores.add(descriptor)

        return res

    class Meta:
        model = Libro
        exclude = ['id', 'descriptores']

class InformeForm(LibroForm):

    class Meta:
        model = Informe
        exclude = ['id', 'descriptores']