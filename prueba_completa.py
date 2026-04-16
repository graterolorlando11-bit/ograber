#!/usr/bin/env python3
import requests
import json

# Tu token (cópialo de antes)
token = '1b36c0682928291c56183ef0e113150df9ae5cb9ae26f35173ca402279779e64'

print("🔑 TU TOKEN:", token)
print("\n" + "="*70)

# 1. VER TODOS LOS DATOS ACTUALES
print("📋 VER TODOS LOS DATOS ACTUALES:")

response = requests.get('http://djangoapi:8000/eval1_ograber/zonas/', headers={'Authorization': f'Token {token}'})
print(f"Zonas: {len(response.json())} total")

response = requests.get('http://djangoapi:8000/eval1_ograber/caminos/', headers={'Authorization': f'Token {token}'})
print(f"Caminos: {len(response.json())} total")

response = requests.get('http://djangoapi:8000/eval1_ograber/arboles/', headers={'Authorization': f'Token {token}'})
print(f"Árboles: {len(response.json())} total")

print("\n" + "="*70)

# 2. INSERTAR NUEVOS DATOS
print("➕ INSERTANDO NUEVOS DATOS:")

# Nueva zona (coordenadas 80-90 para no superponerse)
zona_nueva = {
    "nombre": "Zona Nueva API",
    "tipo": "C",
    "area": 100,
    "perimetro": 40,
    "responsable": "Usuario API",
    "geom": "POLYGON((80 0, 90 0, 90 10, 80 10, 80 0))"
}

response = requests.post(
    'http://djangoapi:8000/eval1_ograber/zonas/',
    json=zona_nueva,
    headers={'Authorization': f'Token {token}'}
)
print(f"✅ Zona creada - Status: {response.status_code}, ID: {response.json().get('id')}")

# Nuevo camino (línea horizontal en Y=25, X=80-90)
camino_nuevo = {
    "nombre": "Camino API",
    "dificultad": "Media",
    "longitud": 10,
    "ancho": 3,
    "material": "Piedra",
    "geom": "LINESTRING(80 25, 90 25)"
}

response = requests.post(
    'http://djangoapi:8000/eval1_ograber/caminos/',
    json=camino_nuevo,
    headers={'Authorization': f'Token {token}'}
)
print(f"✅ Camino creado - Status: {response.status_code}, ID: {response.json().get('id')}")

# Nuevo árbol (dentro de la zona nueva)
arbol_nuevo = {
    "especie": "Pino",
    "altura": 20,
    "diametro": 2,
    "edad": 30,
    "estado": "Excelente",
    "geom": "POINT(85 5)"  # Dentro de zona 80-90, 0-10
}

response = requests.post(
    'http://djangoapi:8000/eval1_ograber/arboles/',
    json=arbol_nuevo,
    headers={'Authorization': f'Token {token}'}
)
print(f"✅ Árbol creado - Status: {response.status_code}, ID: {response.json().get('id')}")

print("\n" + "="*70)

# 3. VERIFICAR QUE SE CREARON
print("🔍 VERIFICANDO DATOS DESPUÉS DE INSERTAR:")

response = requests.get('http://djangoapi:8000/eval1_ograber/zonas/', headers={'Authorization': f'Token {token}'})
zonas = response.json()
print(f"Zonas totales: {len(zonas)}")
for z in zonas[-1:]:  # Mostrar solo la última
    print(f"  Última zona: {z['nombre']} (ID: {z['id']})")

response = requests.get('http://djangoapi:8000/eval1_ograber/caminos/', headers={'Authorization': f'Token {token}'})
caminos = response.json()
print(f"Caminos totales: {len(caminos)}")
for c in caminos[-1:]:
    print(f"  Último camino: {c['nombre']} (ID: {c['id']})")

response = requests.get('http://djangoapi:8000/eval1_ograber/arboles/', headers={'Authorization': f'Token {token}'})
arboles = response.json()
print(f"Árboles totales: {len(arboles)}")
for a in arboles[-1:]:
    print(f"  Último árbol: {a['especie']} (ID: {a['id']})")

print("\n🎉 ¡PRUEBA COMPLETA!")