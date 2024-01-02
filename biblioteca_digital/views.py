from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def bienvenida(request):
    if(request.user.is_authenticated):
        return redirect('busqueda_libros')
    else:
        if(request.method == 'GET'):
            return render(request, 'inicio_sesion.html', {'titulo': 'Bienvenido a la Biblioteca Digital de Indesca'})
        elif(request.method == 'POST'):
            usuario = request.POST.get('usuario', None)
            clave = request.POST.get('password', None)
            user = authenticate(request, username=usuario, password=clave)
            if(user is not None):
                login(request, user)
                return redirect('busqueda_libros')
            else:
                return render(request, 'inicio_sesion.html', {'titulo': 'Bienvenido a la Biblioteca Digital de Indesca', 'error': 'Usuario o contraseña incorrectos.'})
            
def cerrar_sesion(request):
    logout(request)
    return redirect('bienvenida')