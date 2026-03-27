from eval1_ograber.models import Zona
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from django.forms.models import model_to_dict

class ZonasDjango:
    def __init__(self):
        self.snap_grid = 0.0001

    def insert(self, d):
        try:
            # 1. Ajustar a la rejilla (SnapToGrid) usando una consulta rápida
            cur = connection.cursor()
            cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [d['geom'], self.snap_grid])
            geom_snapped = cur.fetchone()[0]

            # 2. Crear el objeto geométrico de Django
            g = GEOSGeometry(geom_snapped, srid=25830)

            if not g.valid:
                return {'ok': False, 'message': 'Geometría inválida', 'data': []}

            # 3. Restricción: Comprobar superposición usando Django ORM (st_relate)
            if Zona.objects.filter(geom__relate=(g, 'T********')).exists():
                return {'ok': False, 'message': f"La zona {d['nombre']} se superpone", 'data': []}

            # 4. Insertar en la base de datos
            d['geom'] = g 
            nueva_zona = Zona(**d) 
            nueva_zona.save()      
            
            return {'ok': True, 'message': 'Zona insertada con Django', 'data': [{'id': nueva_zona.id}]}

        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}
        
    def update(self, d):
        try:
            zona = Zona.objects.get(id=d['id'])
            if 'geom' in d:
                cur = connection.cursor()
                cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [d['geom'], self.snap_grid])
                g = GEOSGeometry(cur.fetchone()[0], srid=25830)

                # Comprobamos solapamiento excluyendo la propia zona
                if Zona.objects.filter(geom__relate=(g, 'T********')).exclude(id=d['id']).exists():
                    return {'ok': False, 'message': 'La zona se superpone', 'data': []}
                zona.geom = g

            if 'nombre' in d: zona.nombre = d['nombre']
            if 'tipo' in d: zona.tipo = d['tipo']
            zona.save()
            return {'ok': True, 'message': 'Zona actualizada', 'data': [{'id': zona.id}]}
        except Zona.DoesNotExist:
            return {'ok': False, 'message': 'Zona no existe', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            zona = Zona.objects.get(id=d['id'])
            zona.delete()
            return {'ok': True, 'message': 'Zona borrada', 'data': [{'id': d['id']}]}
        except Zona.DoesNotExist:
            return {'ok': False, 'message': 'Zona no existe', 'data': []}

    def selectAsDicts(self, d):
        try:
            zona = Zona.objects.get(id=d['id'])
            diccionario = model_to_dict(zona)
            diccionario['geom'] = zona.geom.wkt
            return {'ok': True, 'message': 'Zona recuperada', 'data': [diccionario]}
        except Zona.DoesNotExist:
            return {'ok': False, 'message': 'Zona no encontrada', 'data': []}