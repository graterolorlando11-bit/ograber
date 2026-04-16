from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from eval1_ograber.models import Zona, Camino, Arbol
from eval1_ograber.serializers import ZonaSerializer, CaminoSerializer, ArbolSerializer

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    permission_classes = [IsAuthenticated]

class CaminoViewSet(viewsets.ModelViewSet):
    queryset = Camino.objects.all()
    serializer_class = CaminoSerializer
    permission_classes = [IsAuthenticated]

class ArbolViewSet(viewsets.ModelViewSet):
    queryset = Arbol.objects.all()
    serializer_class = ArbolSerializer
    permission_classes = [IsAuthenticated]


# ===== VISTAS WEB PARA INTERFAZ DE USUARIO =====

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import json

from .models import UserActionLog


# Vista principal - Mapa interactivo
def mapa_principal(request):
    """Vista principal con mapa Leaflet para visualizar datos geoespaciales"""
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'is_admin': request.user.is_staff or request.user.is_superuser if request.user.is_authenticated else False,
    }
    return render(request, 'eval1_ograber/mapa.html', context)


# API para obtener datos geoespaciales (JSON para el mapa)
def obtener_datos_geo(request):
    """API que devuelve todos los datos geoespaciales en formato GeoJSON"""

    # Solo registrar si el usuario está autenticado
    if request.user.is_authenticated:
        UserActionLog.objects.create(
            user=request.user,
            action='VIEW',
            table_name='all',
            ip_address=get_client_ip(request)
        )

    # Obtener todos los datos
    zonas = Zona.objects.all()
    caminos = Camino.objects.all()
    arboles = Arbol.objects.all()

    # Convertir a GeoJSON
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Agregar zonas
    for zona in zonas:
        geojson_data["features"].append({
            "type": "Feature",
            "geometry": json.loads(zona.geom.geojson),
            "properties": {
                "id": zona.id,
                "tipo": "zona",
                "nombre": zona.nombre,
                "tipo_zona": zona.tipo,
                "area": zona.area,
                "responsable": zona.responsable
            }
        })

    # Agregar caminos
    for camino in caminos:
        geojson_data["features"].append({
            "type": "Feature",
            "geometry": json.loads(camino.geom.geojson),
            "properties": {
                "id": camino.id,
                "tipo": "camino",
                "nombre": camino.nombre,
                "dificultad": camino.dificultad,
                "longitud": camino.longitud,
                "material": camino.material
            }
        })

    # Agregar árboles
    for arbol in arboles:
        geojson_data["features"].append({
            "type": "Feature",
            "geometry": json.loads(arbol.geom.geojson),
            "properties": {
                "id": arbol.id,
                "tipo": "arbol",
                "especie": arbol.especie,
                "altura": arbol.altura,
                "edad": arbol.edad,
                "estado": arbol.estado
            }
        })

    return JsonResponse(geojson_data)


# Vista de administración
def admin_panel(request):
    """Panel de administración para CRUD completo"""
    if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
        return render(request, 'eval1_ograber/acceso_denegado.html')

    context = {
        'zonas': Zona.objects.all(),
        'caminos': Camino.objects.all(),
        'arboles': Arbol.objects.all(),
        'logs': UserActionLog.objects.all()[:50] if request.user.is_authenticated else [],  # Últimos 50 logs
        'user': request.user if request.user.is_authenticated else None,
        'is_admin': request.user.is_staff or request.user.is_superuser if request.user.is_authenticated else False,
    }
    return render(request, 'eval1_ograber/admin.html', context)


# Vista de logs de usuario
def mis_logs(request):
    """Vista para que usuarios vean sus propias acciones"""
    if request.user.is_authenticated:
        logs = UserActionLog.objects.filter(user=request.user).order_by('-timestamp')[:100]
    else:
        logs = []
    return render(request, 'eval1_ograber/mis_logs.html', {
        'logs': logs,
        'user': request.user if request.user.is_authenticated else None,
        'is_admin': request.user.is_staff or request.user.is_superuser if request.user.is_authenticated else False,
    })


def get_client_ip(request):
    """Obtener IP del cliente para logs"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip