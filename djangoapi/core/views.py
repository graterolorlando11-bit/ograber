#Django imports
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import random, time

"""
Código	Nombre	Uso típico
200	OK	Petición exitosa (valor por defecto).
201	Created	Se ha creado un recurso (ej. un nuevo usuario).
400	Bad Request	Datos enviados inválidos o mal formateados.
401	Unauthorized	El usuario no está autenticado.
403	Forbidden	Autenticado, pero sin permisos para esa acción.
404	Not Found	El recurso solicitado no existe.
500	Internal Server Error	Error inesperado en tu código Python.

"""

def custom_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")  # O a donde desees redirigir después del logout

def notLoggedIn(request):
    from django.shortcuts import redirect
    # return redirect('/core/login/')
    return redirect('core_login')

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Core. Hello world", "data":[]},status=200)

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        from django.shortcuts import render, redirect
        if request.user.is_authenticated:
            # return redirect('/eval1_ograber/mapa/')
            return redirect('mapa')
        return render(request, 'core/registro.html')

    def post(self, request, *args, **kwargs):
        from django.shortcuts import render, redirect
        from django.contrib.auth.models import User
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin_token = request.POST.get('adminToken', '')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'core/registro.html', {'error': 'El nombre de usuario ya está tomado'})
            
        user = User.objects.create_user(username=username, password=password)
        if admin_token == "SuperMap24":
            user.is_staff = True
            user.save()
            
        return render(request, 'core/registro.html', {'success': '¡Cuenta creada con éxito! Ve al inicio de sesión.'})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        from django.shortcuts import render, redirect
        if request.user.is_authenticated:
            # return redirect('/eval1_ograber/mapa/')
            return redirect('mapa')
        return render(request, 'core/login.html')

    def post(self, request, *args, **kwargs):
        from django.shortcuts import render, redirect
        import time, random
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            # return redirect('/eval1_ograber/mapa/')
            return redirect('mapa')
        else:
            time.sleep(random.uniform(0, 1)) # Delay de seguridad
            return render(request, 'core/login.html', {'error': 'Usuario o contraseña incorrectos'})

class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        from django.shortcuts import redirect
        logout(request) #removes from the header of the request
                            #the the session_id, stored in a cookie
        # return redirect('/core/login/')
        return redirect('core_login')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from django.shortcuts import render
        from eval1_ograber.models import UserActionLog
        logs = UserActionLog.objects.filter(user=request.user).order_by('-timestamp')[:50]
        return render(request, 'core/perfil.html', {'logs': logs})
        
    def post(self, request, *args, **kwargs):
        from django.shortcuts import render, redirect
        from django.contrib.auth import logout
        from eval1_ograber.models import UserActionLog
        from django.contrib.auth.models import User

        action = request.POST.get('action')
        error = None
        success = None
        
        if action == 'update_username':
            new_username = request.POST.get('new_username')
            if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                error = "Ese nombre de usuario ya está ocupado."
            else:
                request.user.username = new_username
                request.user.save()
                success = "Alias actualizado exitosamente."
        
        elif action == 'update_password':
            new_pass = request.POST.get('new_password')
            if new_pass and len(new_pass) > 3:
                request.user.set_password(new_pass)
                request.user.save()
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
                success = "Contraseña cambiada."
            else:
                error = "La contraseña es muy corta."

        elif action == 'delete_account':
            request.user.delete()
            logout(request)
            # return redirect('/core/login/')
            return redirect('core_login')

        logs = UserActionLog.objects.filter(user=request.user).order_by('-timestamp')[:50]
        return render(request, 'core/perfil.html', {'logs': logs, 'error': error, 'success': success})

class IsLoggedIn(View):
    def post(self, request, *args, **kwargs):
        print(request.user.username)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return JsonResponse({"ok":True,"message": "You are authenticated", "data":[{'username':request.user.username}]}, status=200)
        else:
            return JsonResponse({"ok":False,"message": "You are not authenticated", "data":[]}, status=400)
