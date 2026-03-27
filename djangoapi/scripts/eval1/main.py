from scripts.eval1.zonas.zonas_psycopg import ZonasPsycopg
from scripts.eval1.caminos.caminos_psycopg import CaminosPsycopg
from scripts.eval1.arboles.arboles_psycopg import ArbolesPsycopg

def run():
    zonas_db = ZonasPsycopg()
    caminos_db = CaminosPsycopg()
    arboles_db = ArbolesPsycopg()
    
    # Zonas (Cajas separadas de 10x10)
    zonas = [
        {'nombre': 'Z1', 'tipo': 'A', 'area': 100, 'perimetro': 40, 'responsable': 'R1', 'geom': 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))'},
        {'nombre': 'Z2', 'tipo': 'B', 'area': 100, 'perimetro': 40, 'responsable': 'R2', 'geom': 'POLYGON((20 0, 30 0, 30 10, 20 10, 20 0))'},
        {'nombre': 'Z3', 'tipo': 'C', 'area': 100, 'perimetro': 40, 'responsable': 'R3', 'geom': 'POLYGON((40 0, 50 0, 50 10, 40 10, 40 0))'},
        {'nombre': 'Z4', 'tipo': 'D', 'area': 100, 'perimetro': 40, 'responsable': 'R4', 'geom': 'POLYGON((0 20, 10 20, 10 30, 0 30, 0 20))'},
        {'nombre': 'Z5', 'tipo': 'E', 'area': 100, 'perimetro': 40, 'responsable': 'R5', 'geom': 'POLYGON((20 20, 30 20, 30 30, 20 30, 20 20))'}
    ]

    # Caminos (Líneas rectas horizontales)
    caminos = [
        {'nombre': 'C1', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(0 -10, 10 -10)'},
        {'nombre': 'C2', 'dificultad': 'Media', 'longitud': 10, 'ancho': 2, 'material': 'Grava', 'geom': 'LINESTRING(20 -10, 30 -10)'},
        {'nombre': 'C3', 'dificultad': 'Alta', 'longitud': 10, 'ancho': 2, 'material': 'Piedra', 'geom': 'LINESTRING(40 -10, 50 -10)'},
        {'nombre': 'C4', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(0 -20, 10 -20)'},
        {'nombre': 'C5', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Asfalto', 'geom': 'LINESTRING(20 -20, 30 -20)'}
    ]

    # Árboles (Puntos)
    arboles = [
        {'especie': 'Pino', 'altura': 10, 'diametro': 1, 'edad': 50, 'estado': 'Sano', 'geom': 'POINT(5 5)'},
        {'especie': 'Roble', 'altura': 12, 'diametro': 2, 'edad': 80, 'estado': 'Sano', 'geom': 'POINT(25 5)'},
        {'especie': 'Olmo', 'altura': 8, 'diametro': 1, 'edad': 30, 'estado': 'Enfermo', 'geom': 'POINT(45 5)'},
        {'especie': 'Haya', 'altura': 15, 'diametro': 3, 'edad': 100, 'estado': 'Sano', 'geom': 'POINT(5 25)'},
        {'especie': 'Abeto', 'altura': 20, 'diametro': 2, 'edad': 60, 'estado': 'Sano', 'geom': 'POINT(25 25)'}
    ]

    print("--- INSERTANDO ZONAS ---")
    for z in zonas: 
        print(zonas_db.insert(z))
    
    print("\n--- INSERTANDO CAMINOS ---")
    for c in caminos: 
        print(caminos_db.insert(c))
    
    print("\n--- INSERTANDO ÁRBOLES ---")
    for a in arboles: 
        print(arboles_db.insert(a))

    # ACTUALIZANDO ARBOL
    # 1. UPDATE: Diccionario completo + 'id'
    # arbol_para_actualizar = {
    #     'id': 1, # ¡ESTO ES LO NUEVO Y OBLIGATORIO!
    #     'especie': 'Pino Gigante', # Cambiamos el nombre
    #     'altura': 25,              # Cambiamos la altura
    #     'diametro': 3,
    #     'edad': 60,
    #     'estado': 'Muy Sano',
    #     'geom': 'POINT(5 5)'       # Misma coordenada, sigue estando dentro de Z1
    # }
    # print("--- ACTUALIZANDO ÁRBOL ---")
    # print(arboles_db.update(arbol_para_actualizar))

    # 2. SELECT: Solo necesitamos el ID
    arbol_para_ver = {'id': 1}
    print("\n--- VIENDO DATOS DEL ÁRBOL ---")
    print(arboles_db.selectAsDicts(arbol_para_ver))

    # 3. DELETE: Solo necesitamos el ID
    # arbol_para_borrar = {'id': 1}
    # print("\n--- BORRANDO ÁRBOL ---")
    # print(arboles_db.delete(arbol_para_borrar))