from scripts.eval1.myLib.db import Db

class ZonasPsycopg:
    def __init__(self):
        self.snap_grid = 0.0001
        self.db = Db()

    def insert(self, d):
        try:
            # 1. Comprobar superposición (Interior)
            query_interseccion = """
                SELECT id FROM zonas 
                WHERE ST_Relate(geom, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s), 'T********')
            """
            self.db.query(query_interseccion, [d['geom'], self.snap_grid])
            if len(self.db.result) > 0:
                return {'ok': False, 'message': 'El polígono se superpone con una zona existente', 'data': []}

            # 2. Insertar
            query_insert = """
                INSERT INTO zonas (nombre, tipo, area, perimetro, responsable, geom) 
                VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)) 
                RETURNING id
            """
            valores = [d['nombre'], d['tipo'], d['area'], d['perimetro'], d['responsable'], d['geom'], self.snap_grid]
            self.db.query(query_insert, valores)
            
            nuevo_id = dict(self.db.result[0])['id']
            return {'ok': True, 'message': 'Zona insertada', 'data': [{'id': nuevo_id}]}
            
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}
        
    def update(self, d):
        try:
            # Comprobar que la nueva forma no choque con OTRAS zonas (excluimos su propio ID)
            query_interseccion = """
                SELECT id FROM zonas 
                WHERE ST_Relate(geom, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s), 'T********')
                AND id != %s
            """
            self.db.query(query_interseccion, [d['geom'], self.snap_grid, d['id']])
            if len(self.db.result) > 0:
                return {'ok': False, 'message': 'La zona actualizada se superpone con otra', 'data': []}

            query_update = """
                UPDATE zonas 
                SET nombre = %s, tipo = %s, area = %s, perimetro = %s, responsable = %s, geom = ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)
                WHERE id = %s
            """
            valores = [d['nombre'], d['tipo'], d['area'], d['perimetro'], d['responsable'], d['geom'], self.snap_grid, d['id']]
            self.db.query(query_update, valores)
            return {'ok': True, 'message': 'Zona actualizada', 'data': [{'rows_updated': self.db.result}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            self.db.query("DELETE FROM zonas WHERE id = %s", [d['id']])
            return {'ok': True, 'message': 'Zona borrada', 'data': [{'rows_deleted': self.db.result}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def selectAsDicts(self, d):
        try:
            self.db.query("SELECT id, nombre, tipo, area, perimetro, responsable, ST_AsText(geom) as geom FROM zonas WHERE id = %s", [d['id']])
            if len(self.db.result) > 0:
                return {'ok': True, 'message': 'Zona recuperada', 'data': [dict(self.db.result[0])]}
            return {'ok': False, 'message': 'Zona no encontrada', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}