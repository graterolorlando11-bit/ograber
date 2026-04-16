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

def check_overlaps():
    zonas = Zona.objects.all()
    print(f'Encontradas {len(zonas)} zonas')

    for i, zona1 in enumerate(zonas):
        for zona2 in zonas[i+1:]:
            cur = connection.cursor()
            cur.execute('SELECT ST_Overlaps(%s, %s)', [zona1.geom.wkt, zona2.geom.wkt])
            overlaps = cur.fetchone()[0]
            if overlaps:
                print(f'❌ Zonas {zona1.id} y {zona2.id} se superponen')
            else:
                print(f'✅ Zonas {zona1.id} y {zona2.id} NO se superponen')

if __name__ == '__main__':
    check_overlaps()