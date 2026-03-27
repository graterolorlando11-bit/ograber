from scripts.eval1.myLib.db import Db

class CaminosPsycopg:
    def __init__(self):
        self.snap_grid = 0.0001
        self.db = Db()

    def insert(self, d):
        try:
            # 1. Comprobar que no se cruza con otra línea
            query_interseccion = """
                SELECT id FROM caminos 
                WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s))
            """
            self.db.query(query_interseccion, [d['geom'], self.snap_grid])
            if len(self.db.result) > 0:
                return {'ok': False, 'message': f"El camino {d['nombre']} se cruza con otro", 'data': []}

            # 2. Insertar
            query_insert = """
                INSERT INTO caminos (nombre, dificultad, longitud, ancho, material, geom) 
                VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)) 
                RETURNING id
            """
            valores = [d['nombre'], d['dificultad'], d['longitud'], d['ancho'], d['material'], d['geom'], self.snap_grid]
            self.db.query(query_insert, valores)
            
            nuevo_id = dict(self.db.result[0])['id']
            return {'ok': True, 'message': f"Camino {d['nombre']} insertado", 'data': [{'id': nuevo_id}]}
            
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}
        
    def update(self, d):
        try:
            # Comprobar que no se cruce con OTROS caminos
            query_interseccion = """
                SELECT id FROM caminos 
                WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s))
                AND id != %s
            """
            self.db.query(query_interseccion, [d['geom'], self.snap_grid, d['id']])
            if len(self.db.result) > 0:
                return {'ok': False, 'message': 'El camino actualizado se cruza con otro', 'data': []}

            query_update = """
                UPDATE caminos 
                SET nombre = %s, dificultad = %s, longitud = %s, ancho = %s, material = %s, geom = ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)
                WHERE id = %s
            """
            valores = [d['nombre'], d['dificultad'], d['longitud'], d['ancho'], d['material'], d['geom'], self.snap_grid, d['id']]
            self.db.query(query_update, valores)
            return {'ok': True, 'message': 'Camino actualizado', 'data': [{'rows_updated': self.db.result}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            self.db.query("DELETE FROM caminos WHERE id = %s", [d['id']])
            return {'ok': True, 'message': 'Camino borrado', 'data': [{'rows_deleted': self.db.result}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def selectAsDicts(self, d):
        try:
            self.db.query("SELECT id, nombre, dificultad, longitud, ancho, material, ST_AsText(geom) as geom FROM caminos WHERE id = %s", [d['id']])
            if len(self.db.result) > 0:
                return {'ok': True, 'message': 'Camino recuperado', 'data': [dict(self.db.result[0])]}
            return {'ok': False, 'message': 'Camino no encontrado', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}