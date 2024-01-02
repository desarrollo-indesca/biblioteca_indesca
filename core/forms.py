from typing import Any
from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    descriptores = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Separe cada descriptor con el carácter ";"'}))

    def save(self, commit: bool = ...) -> Any:
        res = super().save(commit)
        
        print(res)

        return res

    class Meta:
        model = Libro
        exclude = ['fecha_creacion', 'fecha_actualizacion', 'id', 'descriptores']
