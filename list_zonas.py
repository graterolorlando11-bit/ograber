#!/usr/bin/env python3
import requests
import json

token = '1b36c0682928291c56183ef0e113150df9ae5cb9ae26f35173ca402279779e64'

response = requests.get(
    'http://djangoapi:8000/eval1_ograber/zonas/',
    headers={'Authorization': f'Token {token}'}
)

print('Status Code:', response.status_code)
if response.status_code == 200:
    data = response.json()
    print(f'Total zonas: {len(data)}')
    for zona in data:
        geom_short = zona['geom'][:50] + '...' if len(zona['geom']) > 50 else zona['geom']
        print(f'ID: {zona["id"]}, Nombre: {zona["nombre"]}, Geom: {geom_short}')
else:
    print('Error:', response.text)