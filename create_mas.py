#!/usr/bin/env python3
import requests
import json

token = '1b36c0682928291c56183ef0e113150df9ae5cb9ae26f35173ca402279779e64'

# Crear un camino (línea horizontal en Y=15, X=60-70)
camino = {
    "nombre": "Camino Test 1",
    "dificultad": "Fácil",
    "longitud": 10,
    "ancho": 2,
    "material": "Asfalto",
    "geom": "LINESTRING(60 15, 70 15)"
}

response = requests.post(
    'http://djangoapi:8000/eval1_ograber/caminos/',
    json=camino,
    headers={'Authorization': f'Token {token}'}
)

print("=== CREANDO CAMINO ===")
print("Status Code:", response.status_code)
print("Response Text:")
print(response.text)

# Crear un árbol dentro de la zona que acabamos de crear (Zona Test 1)
arbol = {
    "especie": "Roble",
    "altura": 15,
    "diametro": 3,
    "edad": 50,
    "estado": "Sano",
    "geom": "POINT(65 5)"  # Dentro de la zona 60-70, 0-10
}

response2 = requests.post(
    'http://djangoapi:8000/eval1_ograber/arboles/',
    json=arbol,
    headers={'Authorization': f'Token {token}'}
)

print("\n=== CREANDO ÁRBOL ===")
print("Status Code:", response2.status_code)
print("Response Text:")
print(response2.text)