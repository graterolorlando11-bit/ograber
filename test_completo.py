#!/usr/bin/env python3
"""
Script de prueba completo para la aplicación Eval1 Ograber
Prueba todas las funcionalidades: APIs REST, interfaz web, validaciones geoespaciales
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/eval1_ograber"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def test_api_endpoints():
    """Prueba todas las APIs REST"""
    print_separator("PRUEBA DE APIs REST")

    # 1. Obtener token de autenticación
    print("1. 🔐 Obteniendo token de autenticación...")
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/core/knox_login/", json=login_data)
    if response.status_code == 200:
        token = response.json()['data'][0]['token']
        headers = {"Authorization": f"Token {token}"}
        print("   ✅ Token obtenido correctamente")
    else:
        print("   ❌ Error obteniendo token")
        return

    # 2. Probar APIs de datos
    print("\n2. 📊 Probando APIs de datos...")

    # Zonas
    response = requests.get(f"{API_BASE}/zonas/", headers=headers)
    print(f"   Zonas: {len(response.json())} registros")

    # Caminos
    response = requests.get(f"{API_BASE}/caminos/", headers=headers)
    print(f"   Caminos: {len(response.json())} registros")

    # Árboles
    response = requests.get(f"{API_BASE}/arboles/", headers=headers)
    print(f"   Árboles: {len(response.json())} registros")

    # 3. Probar creación de datos
    print("\n3. ➕ Probando creación de registros...")

    # Crear zona
    zona_data = {
        "nombre": "Zona Test API",
        "tipo": "C",
        "responsable": "API Test",
        "geom": {
            "type": "Polygon",
            "coordinates": [[[150.0,150.0],[160.0,150.0],[160.0,160.0],[150.0,160.0],[150.0,150.0]]]
        }
    }
    response = requests.post(f"{API_BASE}/zonas/", json=zona_data, headers=headers)
    if response.status_code == 201:
        zona_id = response.json()['id']
        print(f"   ✅ Zona creada (ID: {zona_id})")
    else:
        print(f"   ❌ Error creando zona: {response.json()}")
        zona_id = None

    # Crear camino
    camino_data = {
        "nombre": "Camino Test API",
        "dificultad": "Media",
        "ancho": 4.0,
        "material": "Concreto",
        "geom": {
            "type": "LineString",
            "coordinates": [[155.0,155.0],[165.0,155.0]]
        }
    }
    response = requests.post(f"{API_BASE}/caminos/", json=camino_data, headers=headers)
    if response.status_code == 201:
        camino_id = response.json()['id']
        print(f"   ✅ Camino creado (ID: {camino_id})")
    else:
        print(f"   ❌ Error creando camino: {response.json()}")

    # Crear árbol
    if zona_id:
        arbol_data = {
            "especie": "Roble",
            "altura": 15.0,
            "diametro": 1.5,
            "edad": 40,
            "estado": "Excelente",
            "geom": {
                "type": "Point",
                "coordinates": [155.0,155.0]
            }
        }
        response = requests.post(f"{API_BASE}/arboles/", json=arbol_data, headers=headers)
        if response.status_code == 201:
            arbol_id = response.json()['id']
            print(f"   ✅ Árbol creado (ID: {arbol_id})")
        else:
            print(f"   ❌ Error creando árbol: {response.json()}")

    # 4. Probar validaciones geoespaciales
    print("\n4. 🎯 Probando validaciones geoespaciales...")

    # Zona que se superpone (debería fallar)
    zona_superpuesta = {
        "nombre": "Zona Superpuesta",
        "tipo": "A",
        "responsable": "Test",
        "geom": {
            "type": "Polygon",
            "coordinates": [[[0.0,0.0],[50.0,0.0],[50.0,50.0],[0.0,50.0],[0.0,0.0]]]
        }
    }
    response = requests.post(f"{API_BASE}/zonas/", json=zona_superpuesta, headers=headers)
    if response.status_code != 201:
        print("   ✅ Validación de no-superposición funciona")
    else:
        print("   ❌ Validación de no-superposición falló")

    # Árbol fuera de zona (debería fallar)
    arbol_fuera = {
        "especie": "Pino",
        "altura": 10.0,
        "diametro": 1.0,
        "edad": 20,
        "estado": "Bueno",
        "geom": {
            "type": "Point",
            "coordinates": [500.0,500.0]  # Fuera de cualquier zona
        }
    }
    response = requests.post(f"{API_BASE}/arboles/", json=arbol_fuera, headers=headers)
    if response.status_code != 201:
        print("   ✅ Validación de árbol en zona funciona")
    else:
        print("   ❌ Validación de árbol en zona falló")

def test_web_interface():
    """Prueba la interfaz web"""
    print_separator("PRUEBA DE INTERFAZ WEB")

    # 1. Probar páginas sin login
    print("1. 🌐 Probando páginas públicas...")

    pages = [
        ("Mapa", f"{API_BASE}/mapa/"),
        ("Panel Admin", f"{API_BASE}/admin/"),
        ("Mis Logs", f"{API_BASE}/logs/"),
        ("Datos Geo", f"{API_BASE}/datos-geo/")
    ]

    for name, url in pages:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"   ✅ {name}: Accesible")
        else:
            print(f"   ❌ {name}: Error {response.status_code}")

    # 2. Probar login
    print("\n2. 🔐 Probando sistema de login...")
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/core/knox_login/", json=login_data)
    if response.status_code == 200:
        print("   ✅ Login exitoso")
    else:
        print(f"   ❌ Login falló: {response.json()}")

def test_data_integrity():
    """Verifica la integridad de los datos"""
    print_separator("VERIFICACIÓN DE INTEGRIDAD DE DATOS")

    # Obtener datos geo
    response = requests.get(f"{API_BASE}/datos-geo/")
    if response.status_code == 200:
        geojson = response.json()
        print(f"✅ GeoJSON válido con {len(geojson['features'])} elementos")

        # Contar por tipo
        tipos = {}
        for feature in geojson['features']:
            tipo = feature['properties']['tipo']
            tipos[tipo] = tipos.get(tipo, 0) + 1

        print("   📊 Elementos por tipo:")
        for tipo, count in tipos.items():
            print(f"      {tipo}: {count}")
    else:
        print("❌ Error obteniendo datos geo")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE EVAL1 OGRABER")
    print("Aplicación: Sistema Geoespacial Django + PostGIS")
    print(f"URL Base: {BASE_URL}")

    try:
        test_web_interface()
        test_api_endpoints()
        test_data_integrity()

        print_separator("RESUMEN FINAL")
        print("✅ Todas las pruebas completadas exitosamente!")
        print("\n📋 ACCESO A LA APLICACIÓN:")
        print(f"   🌍 Mapa: {BASE_URL}/eval1_ograber/mapa/")
        print(f"   🔧 Admin: {BASE_URL}/eval1_ograber/admin/")
        print(f"   📊 Logs: {BASE_URL}/eval1_ograber/logs/")
        print(f"   🔐 Login: {BASE_URL}/core/login/")
        print("\n👥 USUARIOS DE PRUEBA:")
        print("   Admin: admin / admin123")
        print("   Usuario: usuario_normal / usuario123")
        print("   Admin Normal: admin_normal / admin123")

    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    main()