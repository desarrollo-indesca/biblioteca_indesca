from django.shortcuts import render

def bienvenida(request):
    return render(request, 'inicio_sesion.html', {'titulo': 'Bienvenido a la Biblioteca Digital de Indesca'})