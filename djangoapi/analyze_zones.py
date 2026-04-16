#!/usr/bin/env python
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapi.settings')
django.setup()

from eval1_ograber.models import Zona
from django.db import connection

def analyze_zones():
    zona14 = Zona.objects.get(id=14)
    zona15 = Zona.objects.get(id=15)

    print(f"Zona 14: {zona14.nombre}")
    print(f"  Geometría: {zona14.geom}")
    print(f"  WKT: {zona14.geom.wkt}")
    print()

    print(f"Zona 15: {zona15.nombre}")
    print(f"  Geometría: {zona15.geom}")
    print(f"  WKT: {zona15.geom.wkt}")
    print()

    # Verificar diferentes tipos de intersección
    cur = connection.cursor()

    # ST_Intersects (incluye tocar bordes)
    cur.execute('SELECT ST_Intersects(%s, %s)', [zona14.geom.wkt, zona15.geom.wkt])
    intersects = cur.fetchone()[0]
    print(f"ST_Intersects: {intersects}")

    # ST_Overlaps (solo superposición real)
    cur.execute('SELECT ST_Overlaps(%s, %s)', [zona14.geom.wkt, zona15.geom.wkt])
    overlaps = cur.fetchone()[0]
    print(f"ST_Overlaps: {overlaps}")

    # ST_Touches (solo tocar bordes)
    cur.execute('SELECT ST_Touches(%s, %s)', [zona14.geom.wkt, zona15.geom.wkt])
    touches = cur.fetchone()[0]
    print(f"ST_Touches: {touches}")

    # Área de intersección
    cur.execute('SELECT ST_Area(ST_Intersection(%s, %s))', [zona14.geom.wkt, zona15.geom.wkt])
    intersection_area = cur.fetchone()[0]
    print(f"Área de intersección: {intersection_area}")

if __name__ == '__main__':
    analyze_zones()