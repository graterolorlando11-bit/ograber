from scripts.eval1.zonas.zonas_django import ZonasDjango
from scripts.eval1.caminos.caminos_django import CaminosDjango
from scripts.eval1.arboles.arboles_django import ArbolesDjango

def run():
    zonas_db = ZonasDjango()
    caminos_db = CaminosDjango()
    arboles_db = ArbolesDjango()
    
    # # Creamos un dato nuevo para cada tabla que sabemos que cumple las reglas
    # zona_nueva = {'nombre': 'Z6_Django', 'tipo': 'F', 'area': 100, 'perimetro': 40, 'responsable': 'R6', 'geom': 'POLYGON((0 40, 10 40, 10 50, 0 50, 0 40))'}
    # camino_nuevo = {'nombre': 'C6_Django', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(0 -30, 10 -30)'}
    # arbol_nuevo = {'especie': 'Naranjo_Django', 'altura': 5, 'diametro': 1, 'edad': 10, 'estado': 'Sano', 'geom': 'POINT(5 45)'} # Este punto cae justo dentro de Z6_Django

    # print("--- INSERTANDO CON DJANGO ---")
    # print(zonas_db.insert(zona_nueva))
    # print(caminos_db.insert(camino_nuevo))
    # print(arboles_db.insert(arbol_nuevo))

    # ACTUALIZAMOS ZONAS
    # 1. UPDATE: En nuestro código de Django lo hicimos flexible.
    # Puedes mandarle solo el id y lo que quieres cambiar.
    # zona_para_actualizar = {
    #     'id': 6,
    #     'nombre': 'Z6_Renombrada',
    #     'tipo': 'Z'
    # }
    # print("--- ACTUALIZANDO CON DJANGO ---")
    # print(zonas_db.update(zona_para_actualizar))

    # ACTUALIZAMOS CAMINOS
    camino_actualizar = {
        'id': 5,
        'nombre': 'PRUEBA_DESWEB'
    }
    print("--- ACTUALIZANDO CON DJANGO ---")
    print(caminos_db.update(camino_actualizar))

    # # 2. SELECT: Solo el ID
    # zona_para_ver = {'id': 6}
    # print("\n--- VIENDO DATOS CON DJANGO ---")
    # print(zonas_db.selectAsDicts(zona_para_ver))

    # 3. DELETE: Solo el ID
    # zona_para_borrar = {'id': 6}
    # print("\n--- BORRANDO CON DJANGO ---")
    # print(zonas_db.delete(zona_para_borrar))