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

            # 3. Restricción: Comprobar superposición usando ST_Overlaps
            cur.execute(f"SELECT COUNT(*) FROM {Zona._meta.db_table} WHERE ST_Overlaps(geom, ST_GeomFromText(%s, 25830))", [g.wkt])
            if cur.fetchone()[0] > 0:
                return {'ok': False, 'message': f"La zona {d.get('nombre', '')} se superpone", 'data': []}

            # Metric calculation via coordinate transformation (ETRS89 UTM 30N)
            g_4326 = GEOSGeometry(geom_snapped, srid=4326)
            g_metric = g_4326.transform(25830, clone=True)

            # 4. Asignación algorítmica forzosa y guardado
            d['geom'] = g 
            d['area'] = round(g_metric.area, 2)
            d['perimetro'] = round(g_metric.length, 2)
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
                cur.execute(f"SELECT COUNT(*) FROM {Zona._meta.db_table} WHERE id != %s AND ST_Overlaps(geom, ST_GeomFromText(%s, 25830))", [d['id'], g.wkt])
                if cur.fetchone()[0] > 0:
                    return {'ok': False, 'message': 'La zona se superpone', 'data': []}
                
                # Transform to compute metrics
                g_4326 = GEOSGeometry(cur.fetchone()[0] if 'cur.fetchone()[0]' in locals() else d['geom'], srid=4326)
                # Note: cur.fetchone() is consumed from the overlapping query! We must use the original g
                g_metric = GEOSGeometry(g.wkb, srid=4326).transform(25830, clone=True)

                zona.geom = g
                zona.area = round(g_metric.area, 2)
                zona.perimetro = round(g_metric.length, 2)

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