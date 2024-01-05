from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def bienvenida(request):
    '''
    Resumen:
        Vista para la página de bienvenida.

    Atributos:
        request: HttpRequest -> Solicitud HTTP. Solo acepta POST y GET

    Retorna:
        HttpResponse -> Redirección si el usuario está autenticado, formulario de inicio de sesión si no, redirección si autentica exitosamente, formulario con error si no.
    '''
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
    '''
    Resumen:
        Vista para cerrar sesión.
        
    Atributos:
        request: HttpRequest -> Solicitud HTTP. Solo acepta POST y GET.

    Retorna:
        HttpResponse -> Redirección a la página de bienvenida.
    '''
    logout(request)
    return redirect('bienvenida')