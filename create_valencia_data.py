#!/usr/bin/env python3
"""
Script para crear datos realistas de Valencia, España
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapi.settings')
django.setup()

from eval1_ograber.models import Zona, Camino, Arbol
from django.contrib.gis.geos import Polygon, LineString, Point

def main():
    print('🧹 Limpiando datos existentes...')
    Zona.objects.all().delete()
    Camino.objects.all().delete()
    Arbol.objects.all().delete()

    print('🌳 Creando datos realistas de Valencia, España...')

    # Coordenadas base de Valencia (centro aproximado)
    # 39.4699°N, -0.3763°E
    base_lat, base_lon = 39.4699, -0.3763

    # ===== ZONAS =====
    print('\n🏞️ Creando zonas...')

    # Parque Central de Valencia
    parque_coords = [
        (base_lon - 0.01, base_lat - 0.005),  # Suroeste
        (base_lon + 0.01, base_lat - 0.005),  # Sureste
        (base_lon + 0.01, base_lat + 0.005),  # Noreste
        (base_lon - 0.01, base_lat + 0.005),  # Noroeste
        (base_lon - 0.01, base_lat - 0.005),  # Cerrar
    ]

    parque = Zona.objects.create(
        nombre='Parque Central de Valencia',
        tipo='A',
        responsable='Ayuntamiento de Valencia',
        geom=Polygon(parque_coords)
    )
    print(f'   ✅ Parque Central creado (ID: {parque.id})')

    # Jardín Botánico
    jardin_coords = [
        (base_lon - 0.008, base_lat + 0.002),  # Suroeste
        (base_lon - 0.003, base_lat + 0.002),  # Sureste
        (base_lon - 0.003, base_lat + 0.007),  # Noreste
        (base_lon - 0.008, base_lat + 0.007),  # Noroeste
        (base_lon - 0.008, base_lat + 0.002),  # Cerrar
    ]

    jardin = Zona.objects.create(
        nombre='Jardín Botánico',
        tipo='B',
        responsable='Universidad de Valencia',
        geom=Polygon(jardin_coords)
    )
    print(f'   ✅ Jardín Botánico creado (ID: {jardin.id})')

    # ===== CAMINOS =====
    print('\n🚶 Creando caminos...')

    # Camino principal norte-sur
    camino_principal_coords = [
        (base_lon, base_lat - 0.004),  # Sur
        (base_lon, base_lat + 0.004),  # Norte
    ]

    camino_principal = Camino.objects.create(
        nombre='Camino Principal Norte-Sur',
        dificultad='Fácil',
        ancho=3.0,
        material='Piedra',
        geom=LineString(camino_principal_coords)
    )
    print(f'   ✅ Camino principal creado (ID: {camino_principal.id})')

    # Camino este-oeste
    camino_lateral_coords = [
        (base_lon - 0.008, base_lat),  # Oeste
        (base_lon + 0.008, base_lat),  # Este
    ]

    camino_lateral = Camino.objects.create(
        nombre='Camino Este-Oeste',
        dificultad='Media',
        ancho=2.5,
        material='Asfalto',
        geom=LineString(camino_lateral_coords)
    )
    print(f'   ✅ Camino lateral creado (ID: {camino_lateral.id})')

    # Sendero del jardín
    sendero_coords = [
        (base_lon - 0.007, base_lat + 0.003),  # Inicio
        (base_lon - 0.005, base_lat + 0.005),  # Medio
        (base_lon - 0.004, base_lat + 0.003),  # Fin
    ]

    sendero = Camino.objects.create(
        nombre='Sendero del Jardín',
        dificultad='Alta',
        ancho=1.5,
        material='Tierra',
        geom=LineString(sendero_coords)
    )
    print(f'   ✅ Sendero del jardín creado (ID: {sendero.id})')

    # ===== ÁRBOLES =====
    print('\n🌲 Creando árboles...')

    # Árboles en el parque principal
    arboles_parque = [
        {'especie': 'Pino', 'altura': 15.0, 'diametro': 1.2, 'edad': 45, 'estado': 'Excelente', 'pos': (base_lon - 0.005, base_lat)},
        {'especie': 'Roble', 'altura': 12.0, 'diametro': 1.8, 'edad': 60, 'estado': 'Bueno', 'pos': (base_lon + 0.005, base_lat - 0.002)},
        {'especie': 'Castaño', 'altura': 10.0, 'diametro': 1.0, 'edad': 35, 'estado': 'Excelente', 'pos': (base_lon, base_lat + 0.002)},
        {'especie': 'Palmera', 'altura': 8.0, 'diametro': 0.8, 'edad': 25, 'estado': 'Bueno', 'pos': (base_lon - 0.003, base_lat - 0.002)},
        {'especie': 'Olivo', 'altura': 6.0, 'diametro': 0.9, 'edad': 40, 'estado': 'Regular', 'pos': (base_lon + 0.003, base_lat + 0.002)},
    ]

    for i, arbol_data in enumerate(arboles_parque, 1):
        arbol = Arbol.objects.create(
            especie=arbol_data['especie'],
            altura=arbol_data['altura'],
            diametro=arbol_data['diametro'],
            edad=arbol_data['edad'],
            estado=arbol_data['estado'],
            geom=Point(arbol_data['pos'])
        )
        print(f'   ✅ Árbol {i} ({arbol_data["especie"]}): ID {arbol.id}')

    # Árboles en el jardín botánico
    arboles_jardin = [
        {'especie': 'Magnolia', 'altura': 5.0, 'diametro': 0.6, 'edad': 15, 'estado': 'Excelente', 'pos': (base_lon - 0.006, base_lat + 0.004)},
        {'especie': 'Jazmín', 'altura': 3.0, 'diametro': 0.4, 'edad': 10, 'estado': 'Bueno', 'pos': (base_lon - 0.005, base_lat + 0.003)},
        {'especie': 'Rosa', 'altura': 2.0, 'diametro': 0.3, 'edad': 8, 'estado': 'Excelente', 'pos': (base_lon - 0.004, base_lat + 0.005)},
    ]

    for i, arbol_data in enumerate(arboles_jardin, 6):
        arbol = Arbol.objects.create(
            especie=arbol_data['especie'],
            altura=arbol_data['altura'],
            diametro=arbol_data['diametro'],
            edad=arbol_data['edad'],
            estado=arbol_data['estado'],
            geom=Point(arbol_data['pos'])
        )
        print(f'   ✅ Árbol {i} ({arbol_data["especie"]}): ID {arbol.id}')

    # ===== RESUMEN =====
    print('\n📊 RESUMEN FINAL:')
    print(f'   🏞️  Zonas: {Zona.objects.count()}')
    print(f'   🚶 Caminos: {Camino.objects.count()}')
    print(f'   🌲 Árboles: {Arbol.objects.count()}')
    print('\n🎯 Ubicación: Valencia, España (39.47°N, -0.38°E)')
    print('✅ Todos los datos creados exitosamente!')

if __name__ == "__main__":
    main()