#!/usr/bin/env python3
import requests
import json

token = '1b36c0682928291c56183ef0e113150df9ae5cb9ae26f35173ca402279779e64'

# Zona que SÍ se superpone con Z1 (coordenadas 0-10, que ya existe)
zona_superpuesta = {
    "nombre": "Zona Conflictiva",
    "tipo": "B",
    "area": 100,
    "perimetro": 40,
    "responsable": "Test",
    "geom": "POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))"  # Misma que Z1
}

response = requests.post(
    'http://djangoapi:8000/eval1_ograber/zonas/',
    json=zona_superpuesta,
    headers={'Authorization': f'Token {token}'}
)

print("=== PROBANDO VALIDACIÓN (debería dar 400, no 500) ===")
print("Status Code:", response.status_code)
print("Response Text:")
print(response.text)