from scripts.eval1.zonas.zonas_django import ZonasDjango
from scripts.eval1.arboles.arboles_psycopg import ArbolesPsycopg
from scripts.eval1.caminos.caminos_django import CaminosDjango

def run():
    z_dj = ZonasDjango()
    a_psy = ArbolesPsycopg()
    c_dj = CaminosDjango()

    print("\n" + "="*50)
    print(" 1. DEMOSTRACIÓN ZONAS (DJANGO)")
    print("="*50)
    
    # ÉXITO: Insertamos una zona nueva
    zona_ok = {'nombre': 'Zona_Defensa', 'tipo': 'A', 'area': 100, 'perimetro': 40, 'responsable': 'Yo', 'geom': 'POLYGON((500 500, 510 500, 510 510, 500 510, 500 500))'}
    print("[INTENTO] Insertar Zona válida:")
    res_zona = z_dj.insert(zona_ok)
    print("-> RESULTADO:", res_zona)
    id_zona = res_zona['data'][0]['id']

    # RESTRICCIÓN: Intentamos meter otra que la pise (fíjate que las coordenadas se solapan)
    zona_fail = {'nombre': 'Zona_Trampa', 'tipo': 'B', 'geom': 'POLYGON((505 505, 515 505, 515 515, 505 515, 505 505))'}
    print("\n[INTENTO] Insertar Zona superpuesta (Debe ser bloqueado por ST_Relate):")
    print("-> RESULTADO:", z_dj.insert(zona_fail))


    print("\n" + "="*50)
    print(" 2. DEMOSTRACIÓN ÁRBOLES (PSYCOPG)")
    print("="*50)

    # RESTRICCIÓN: Intentamos meter un árbol en el medio de la nada (fuera de zonas)
    arbol_fail = {'especie': 'Roble', 'altura': 10, 'diametro': 1, 'edad': 5, 'estado': 'Sano', 'geom': 'POINT(999 999)'}
    print("[INTENTO] Insertar Árbol fuera del parque (Debe ser bloqueado por ST_Within):")
    print("-> RESULTADO:", a_psy.insert(arbol_fail))

    # ÉXITO: Lo metemos justo en el centro de la 'Zona_Defensa' que acabamos de crear
    arbol_ok = {'especie': 'Roble', 'altura': 10, 'diametro': 1, 'edad': 5, 'estado': 'Sano', 'geom': 'POINT(505 505)'}
    print("\n[INTENTO] Insertar Árbol dentro de la zona válida:")
    res_arbol = a_psy.insert(arbol_ok)
    print("-> RESULTADO:", res_arbol)
    id_arbol = res_arbol['data'][0]['id']

    # UPDATE: Modificamos el estado del árbol
    arbol_update = {'id': id_arbol, 'especie': 'Roble_Viejo', 'estado': 'Seco', 'geom': 'POINT(506 506)'}
    print("\n[INTENTO] Actualizar estado y mover árbol dentro de la misma zona:")
    print("-> RESULTADO:", a_psy.update(arbol_update))


    print("\n" + "="*50)
    print(" 3. DEMOSTRACIÓN CAMINOS Y BORRADO")
    print("="*50)

    # ÉXITO: Creamos un camino
    camino_ok = {'nombre': 'Ruta_Escape', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(500 490, 510 490)'}
    print("[INTENTO] Insertar Camino válido:")
    res_camino = c_dj.insert(camino_ok)
    print("-> RESULTADO:", res_camino)
    id_camino = res_camino['data'][0]['id']

    # DELETE: Borramos todo para dejar la base de datos limpia tras la demo
    print("\n[LIMPIEZA] Borrando datos generados en la demo...")
    print("-> Borrar Árbol:", a_psy.delete({'id': id_arbol}))
    print("-> Borrar Camino:", c_dj.delete({'id': id_camino}))
    print("-> Borrar Zona:", z_dj.delete({'id': id_zona}))
    print("\n¡DEMOSTRACIÓN FINALIZADA CON ÉXITO!")