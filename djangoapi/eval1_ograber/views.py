from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from eval1_ograber.models import Zona, Camino, Arbol, UserActionLog
from eval1_ograber.serializers import ZonaSerializer, CaminoSerializer, ArbolSerializer
from scripts.eval1.zonas.zonas_django import ZonasDjango
from scripts.eval1.caminos.caminos_django import CaminosDjango
from scripts.eval1.arboles.arboles_django import ArbolesDjango

import json
from django.forms.models import model_to_dict

def get_db_dict(table, pk):
    try:
        obj = None
        if table == 'zonas': obj = Zona.objects.get(pk=pk)
        elif table == 'caminos': obj = Camino.objects.get(pk=pk)
        elif table == 'arboles': obj = Arbol.objects.get(pk=pk)
        if obj:
            d = model_to_dict(obj)
            d['geom'] = obj.geom.geojson if obj.geom else None
            return d
    except Exception:
        pass
    return None

def log_audit_action(request, table, action, res, obj_id_fallback=None, before_state=None, after_state=None):
    if not request.user.is_authenticated: return
    obj_id = obj_id_fallback
    if res.get('ok') and res.get('data'):
        obj_id = res['data'][0].get('id', obj_id)
        
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    details = {}
    if before_state: details['before'] = before_state
    if after_state: details['after'] = after_state

    UserActionLog.objects.create(
        user=request.user,
        action=action,
        table_name=table,
        object_id=obj_id,
        ip_address=ip,
        details=json.dumps(details) if details else ""
    )

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        d = request.data.copy()
        res = ZonasDjango().insert(d)
        if res.get('ok'):
            pk = res['data'][0]['id']
            after_state = get_db_dict('zonas', pk)
            log_audit_action(request, 'zonas', 'CREATE', res, after_state=after_state)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        d = request.data.copy()
        pk = kwargs.get('pk')
        if 'id' not in d: d['id'] = pk
        before_state = get_db_dict('zonas', pk)
        res = ZonasDjango().update(d)
        if res.get('ok'):
            after_state = get_db_dict('zonas', pk)
            log_audit_action(request, 'zonas', 'UPDATE', res, before_state=before_state, after_state=after_state)
            return Response(res, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        d = {'id': pk}
        before_state = get_db_dict('zonas', pk)
        res = ZonasDjango().delete(d)
        if res.get('ok'):
            log_audit_action(request, 'zonas', 'DELETE', res, obj_id_fallback=pk, before_state=before_state)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

class CaminoViewSet(viewsets.ModelViewSet):
    queryset = Camino.objects.all()
    serializer_class = CaminoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        res = CaminosDjango().insert(request.data.copy())
        if res.get('ok'):
            pk = res['data'][0]['id']
            after_state = get_db_dict('caminos', pk)
            log_audit_action(request, 'caminos', 'CREATE', res, after_state=after_state)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        d = request.data.copy()
        pk = kwargs.get('pk')
        if 'id' not in d: d['id'] = pk
        before_state = get_db_dict('caminos', pk)
        res = CaminosDjango().update(d)
        if res.get('ok'):
            after_state = get_db_dict('caminos', pk)
            log_audit_action(request, 'caminos', 'UPDATE', res, before_state=before_state, after_state=after_state)
            return Response(res, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        d = {'id': pk}
        before_state = get_db_dict('caminos', pk)
        res = CaminosDjango().delete(d)
        if res.get('ok'):
            log_audit_action(request, 'caminos', 'DELETE', res, obj_id_fallback=pk, before_state=before_state)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

class ArbolViewSet(viewsets.ModelViewSet):
    queryset = Arbol.objects.all()
    serializer_class = ArbolSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        res = ArbolesDjango().insert(request.data.copy())
        if res.get('ok'):
            pk = res['data'][0]['id']
            after_state = get_db_dict('arboles', pk)
            log_audit_action(request, 'arboles', 'CREATE', res, after_state=after_state)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        d = request.data.copy()
        pk = kwargs.get('pk')
        if 'id' not in d: d['id'] = pk
        before_state = get_db_dict('arboles', pk)
        res = ArbolesDjango().update(d)
        if res.get('ok'):
            after_state = get_db_dict('arboles', pk)
            log_audit_action(request, 'arboles', 'UPDATE', res, before_state=before_state, after_state=after_state)
            return Response(res, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        d = {'id': pk}
        before_state = get_db_dict('arboles', pk)
        res = ArbolesDjango().delete(d)
        if res.get('ok'):
            log_audit_action(request, 'arboles', 'DELETE', res, obj_id_fallback=pk, before_state=before_state)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


# ===== VISTAS WEB PARA INTERFAZ DE USUARIO =====

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import json

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
    # Evitamos loguear SELECT individualmente porque ahogaría la bd.

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
        'logs': UserActionLog.objects.all()[:50] if request.user.is_authenticated else [],
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