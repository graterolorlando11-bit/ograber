from eval1_ograber.models import Arbol, Zona
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from django.forms.models import model_to_dict

class ArbolesDjango:
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

            # 2. Restricción: El árbol debe estar DENTRO de una zona
            if not Zona.objects.filter(geom__contains=g).exists():
                return {'ok': False, 'message': f"El árbol {d['especie']} está fuera de las zonas", 'data': []}

            # 3. Guardar
            d['geom'] = g 
            nuevo_arbol = Arbol(**d) 
            nuevo_arbol.save()      
            
            return {'ok': True, 'message': 'Árbol insertado con Django', 'data': [{'id': nuevo_arbol.id}]}

        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def update(self, d):
        try:
            # 1. Buscar el objeto que queremos actualizar
            arbol = Arbol.objects.get(id=d['id'])

            # 2. Si el diccionario trae una geometría nueva, hay que validarla
            if 'geom' in d:
                cur = connection.cursor()
                cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [d['geom'], self.snap_grid])
                g = GEOSGeometry(cur.fetchone()[0], srid=25830)

                # Restricción: ¿El nuevo sitio sigue dentro de una zona?
                if not Zona.objects.filter(geom__contains=g).exists():
                    return {'ok': False, 'message': 'El nuevo punto está fuera de las zonas', 'data': []}
                
                arbol.geom = g # Actualizamos la geometría en el objeto

            # 3. Actualizamos los demás datos si vienen en el diccionario
            if 'especie' in d: arbol.especie = d['especie']
            if 'estado' in d: arbol.estado = d['estado']
            
            # 4. Guardar los cambios en la base de datos
            arbol.save()
            return {'ok': True, 'message': 'Árbol actualizado', 'data': [{'id': arbol.id}]}

        except Arbol.DoesNotExist:
            return {'ok': False, 'message': 'El árbol no existe', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            # Buscamos y disparamos el borrado
            arbol = Arbol.objects.get(id=d['id'])
            arbol.delete()
            return {'ok': True, 'message': 'Árbol borrado correctamente', 'data': [{'id': d['id']}]}
            
        except Arbol.DoesNotExist:
            return {'ok': False, 'message': 'El árbol no existe', 'data': []}

    def selectAsDicts(self, d):
        try:
            # Buscamos el objeto
            arbol = Arbol.objects.get(id=d['id'])
            
            # Django tiene una función mágica para convertir el objeto a diccionario
            diccionario = model_to_dict(arbol)
            
            # La geometría hay que pasarla a texto (WKT) para que se pueda leer bien en el JSON
            diccionario['geom'] = arbol.geom.wkt 
            
            return {'ok': True, 'message': 'Árbol recuperado', 'data': [diccionario]}
            
        except Arbol.DoesNotExist:
            return {'ok': False, 'message': 'El árbol no existe', 'data': []}