from scripts.eval1.myLib.db import Db

class ArbolesPsycopg:
    def __init__(self):
        self.snap_grid = 0.0001
        self.db = Db()

    def insert(self, d):
        try:
            # 1. Comprobar que el punto está DENTRO de alguna zona
            query_dentro = """
                SELECT id FROM zonas 
                WHERE ST_Within(ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s), geom)
            """
            self.db.query(query_dentro, [d['geom'], self.snap_grid])
            if len(self.db.result) == 0:
                return {'ok': False, 'message': f"El árbol {d['especie']} está fuera de las zonas", 'data': []}

            # 2. Insertar
            query_insert = """
                INSERT INTO arboles (especie, altura, diametro, edad, estado, geom) 
                VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)) 
                RETURNING id
            """
            valores = [d['especie'], d['altura'], d['diametro'], d['edad'], d['estado'], d['geom'], self.snap_grid]
            self.db.query(query_insert, valores)
            
            nuevo_id = dict(self.db.result[0])['id']
            return {'ok': True, 'message': f"Árbol {d['especie']} insertado", 'data': [{'id': nuevo_id}]}
            
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}
        
    def update(self, d):
        try:
            # 1. Comprobar que las nuevas coordenadas siguen estando DENTRO de alguna zona
            query_dentro = """
                SELECT id FROM zonas 
                WHERE ST_Within(ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s), geom)
            """
            self.db.query(query_dentro, [d['geom'], self.snap_grid])
            if len(self.db.result) == 0:
                return {'ok': False, 'message': 'El árbol actualizado quedaría fuera de las zonas', 'data': []}

            # 2. Actualizar todos los campos
            query_update = """
                UPDATE arboles 
                SET especie = %s, altura = %s, diametro = %s, edad = %s, estado = %s, geom = ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)
                WHERE id = %s
            """
            valores = [d['especie'], d['altura'], d['diametro'], d['edad'], d['estado'], d['geom'], self.snap_grid, d['id']]
            self.db.query(query_update, valores)
            
            return {'ok': True, 'message': 'Árbol actualizado', 'data': [{'rows_updated': self.db.result}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            self.db.query("DELETE FROM arboles WHERE id = %s", [d['id']])
            return {'ok': True, 'message': 'Árbol borrado', 'data': [{'rows_deleted': self.db.result}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def selectAsDicts(self, d):
        try:
            # Recuerda el ST_AsText para que la geometría sea legible
            self.db.query("SELECT id, especie, altura, diametro, edad, estado, ST_AsText(geom) as geom FROM arboles WHERE id = %s", [d['id']])
            if len(self.db.result) > 0:
                return {'ok': True, 'message': 'Árbol recuperado', 'data': [dict(self.db.result[0])]}
            return {'ok': False, 'message': 'Árbol no encontrado', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}