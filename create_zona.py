#!/usr/bin/env python3
import requests
import json

token = '1b36c0682928291c56183ef0e113150df9ae5cb9ae26f35173ca402279779e64'

# Zona que NO se superpone (coordenadas 60-70)
zona = {
    "nombre": "Zona Test 1",
    "tipo": "A",
    "area": 100,
    "perimetro": 40,
    "responsable": "Admin",
    "geom": "POLYGON((60 0, 70 0, 70 10, 60 10, 60 0))"
}

response = requests.post(
    'http://djangoapi:8000/eval1_ograber/zonas/',
    json=zona,
    headers={'Authorization': f'Token {token}'}
)

print("Status Code:", response.status_code)
print("Response Text:")
print(response.text)