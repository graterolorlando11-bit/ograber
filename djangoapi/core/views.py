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
    return JsonResponse({"ok":False,"message": "You are not logged in", "data":[]},status=400)

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Core. Hello world", "data":[]},status=200)

class LoginView(View):
    def get(self, request, *args, **kwargs):
        """Mostrar formulario de login"""
        if request.user.is_authenticated:
            return JsonResponse({"ok":True,"message": f"The user {request.user.username} already is authenticated", "data":[{'username':request.user.username}]}, status=200)

        # Mostrar formulario HTML simple
        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Iniciar Sesión - Eval1 Ograber</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h4 class="mb-0">🔐 Iniciar Sesión</h4>
                            </div>
                            <div class="card-body">
                                <form method="post" action="/core/login/">
                                    {% csrf_token %}
                                    <div class="mb-3">
                                        <label for="username" class="form-label">Usuario</label>
                                        <input type="text" class="form-control" id="username" name="username" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="password" class="form-label">Contraseña</label>
                                        <input type="password" class="form-control" id="password" name="password" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary w-100">Iniciar Sesión</button>
                                </form>

                                <hr>
                                <div class="text-center">
                                    <a href="/eval1_ograber/mapa/" class="btn btn-secondary">Volver al Mapa</a>
                                </div>

                                <div class="mt-3">
                                    <h6>Usuarios de prueba:</h6>
                                    <small class="text-muted">
                                        • admin / admin123 (Superusuario)<br>
                                        • usuario_normal / usuario123 (Usuario normal)<br>
                                        • admin_normal / admin123 (Staff)
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/eval1_ograber/mapa/')

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/eval1_ograber/mapa/')
        else:
            # Delay para seguridad
            seconds = random.uniform(0, 1)
            time.sleep(seconds)

            # Mostrar formulario con error
            html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Iniciar Sesión - Eval1 Ograber</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="bg-light">
                <div class="container mt-5">
                    <div class="row justify-content-center">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header bg-danger text-white">
                                    <h4 class="mb-0">❌ Error de Inicio de Sesión</h4>
                                </div>
                                <div class="card-body">
                                    <div class="alert alert-danger">
                                        <strong>Usuario o contraseña incorrectos</strong>
                                    </div>
                                    <form method="post" action="/core/login/">
                                        {% csrf_token %}
                                        <div class="mb-3">
                                            <label for="username" class="form-label">Usuario</label>
                                            <input type="text" class="form-control" id="username" name="username" value="{username}" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="password" class="form-label">Contraseña</label>
                                            <input type="password" class="form-control" id="password" name="password" required>
                                        </div>
                                        <button type="submit" class="btn btn-primary w-100">Intentar de Nuevo</button>
                                    </form>

                                    <hr>
                                    <div class="text-center">
                                        <a href="/eval1_ograber/mapa/" class="btn btn-secondary">Volver al Mapa</a>
                                    </div>

                                    <div class="mt-3">
                                        <h6>Usuarios de prueba:</h6>
                                        <small class="text-muted">
                                            • admin / admin123 (Superusuario)<br>
                                            • usuario_normal / usuario123 (Usuario normal)<br>
                                            • admin_normal / admin123 (Staff)
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """.format(username=username or "")
            return HttpResponse(html)

class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username=request.user.username
        logout(request) #removes from the header of the request
                            #the the session_id, stored in a cookie
        return JsonResponse({"ok":True,"message": "The user {0} is now logged out".format(username), "data":[]}, status=200)

class IsLoggedIn(View):
    def post(self, request, *args, **kwargs):
        print(request.user.username)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return JsonResponse({"ok":True,"message": "You are authenticated", "data":[{'username':request.user.username}]}, status=200)
        else:
            return JsonResponse({"ok":False,"message": "You are not authenticated", "data":[]}, status=400)
