from eval1_ograber.models import Camino
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from django.forms.models import model_to_dict

class CaminosDjango:
    def __init__(self):
        self.snap_grid = 0.0001

    def insert(self, d):
        try:
            # 1. Ajustar a la rejilla
            cur = connection.cursor()
            cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [d['geom'], self.snap_grid])
            geom_snapped = cur.fetchone()[0]

            g = GEOSGeometry(geom_snapped, srid=25830)

            if not g.valid:
                return {'ok': False, 'message': 'Geometría inválida', 'data': []}

            # 2. Restricción: Que no se cruce con otro camino
            if Camino.objects.filter(geom__intersects=g).exists():
                return {'ok': False, 'message': f"El camino {d['nombre']} se cruza con otro", 'data': []}

            # 3. Guardar
            d['geom'] = g 
            nuevo_camino = Camino(**d) 
            nuevo_camino.save()      
            
            return {'ok': True, 'message': 'Camino insertado con Django', 'data': [{'id': nuevo_camino.id}]}

        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}
        
    def update(self, d):
        try:
            camino = Camino.objects.get(id=d['id'])
            if 'geom' in d:
                cur = connection.cursor()
                cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [d['geom'], self.snap_grid])
                g = GEOSGeometry(cur.fetchone()[0], srid=25830)

                if Camino.objects.filter(geom__intersects=g).exclude(id=d['id']).exists():
                    return {'ok': False, 'message': 'El camino se cruza', 'data': []}
                camino.geom = g

            if 'nombre' in d: camino.nombre = d['nombre']
            if 'dificultad' in d: camino.dificultad = d['dificultad']
            camino.save()
            return {'ok': True, 'message': 'Camino actualizado', 'data': [{'id': camino.id}]}
        except Camino.DoesNotExist:
            return {'ok': False, 'message': 'Camino no existe', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            camino = Camino.objects.get(id=d['id'])
            camino.delete()
            return {'ok': True, 'message': 'Camino borrado', 'data': [{'id': d['id']}]}
        except Camino.DoesNotExist:
            return {'ok': False, 'message': 'Camino no existe', 'data': []}

    def selectAsDicts(self, d):
        try:
            camino = Camino.objects.get(id=d['id'])
            diccionario = model_to_dict(camino)
            diccionario['geom'] = camino.geom.wkt
            return {'ok': True, 'message': 'Camino recuperado', 'data': [diccionario]}
        except Camino.DoesNotExist:
            return {'ok': False, 'message': 'Camino no encontrado', 'data': []}