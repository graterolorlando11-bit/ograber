from scripts.eval1.zonas.zonas_django import ZonasDjango
from scripts.eval1.zonas.zonas_psycopg import ZonasPsycopg
from scripts.eval1.caminos.caminos_django import CaminosDjango
from scripts.eval1.caminos.caminos_psycopg import CaminosPsycopg
from scripts.eval1.arboles.arboles_django import ArbolesDjango
from scripts.eval1.arboles.arboles_psycopg import ArbolesPsycopg

def run():
    # Instanciamos nuestras 6 herramientas
    z_dj = ZonasDjango()
    z_psy = ZonasPsycopg()
    c_dj = CaminosDjango()
    c_psy = CaminosPsycopg()
    a_dj = ArbolesDjango()
    a_psy = ArbolesPsycopg()

    print("\n" + "="*50)
    print(" 1. PRUEBAS DE ZONAS (POLÍGONOS)")
    print("="*50)
    
    # Insert ZONA DJANGO (en la coordenada 100,100)
    zona_ok = {'nombre': 'Zona_Test', 'tipo': 'Test', 'area': 100, 'perimetro': 40, 'responsable': 'Yo', 'geom': 'POLYGON((100 100, 110 100, 110 110, 100 110, 100 100))'}
    print("-> INSERT (Django) Zona válida:")
    res_z_insert = z_dj.insert(zona_ok)
    print(res_z_insert)
    id_zona = res_z_insert['data'][0]['id'] # Guardamos el ID que nos ha dado la base de datos

    # RESTRICCION DE SOLAPE (Empieza en el 105)
    zona_fail = {'nombre': 'Zona_Fail', 'tipo': 'Test', 'area': 100, 'perimetro': 40, 'responsable': 'Yo', 'geom': 'POLYGON((105 105, 115 105, 115 115, 105 115, 105 105))'}
    print("\n-> INSERT (Psycopg) Zona que se superpone (DEBE FALLAR):")
    print(z_psy.insert(zona_fail))

    print("\n" + "="*50)
    print(" 2. PRUEBAS DE ÁRBOLES (PUNTOS)")
    print("="*50)

    # Intentamos meter un árbol en la coordenada 200,200 (fuera del parque)
    arbol_fail = {'especie': 'Pino_Fail', 'altura': 10, 'diametro': 1, 'edad': 50, 'estado': 'Sano', 'geom': 'POINT(200 200)'}
    print("-> INSERT (Psycopg) Árbol fuera de zonas (DEBE FALLAR):")
    print(a_psy.insert(arbol_fail))

    # Metemos un árbol justo en el centro de la 'Zona_Test' que creamos antes (105, 105)
    arbol_ok = {'especie': 'Pino_Test', 'altura': 10, 'diametro': 1, 'edad': 50, 'estado': 'Sano', 'geom': 'POINT(105 105)'}
    print("\n-> INSERT (Django) Árbol dentro de zona:")
    res_a_insert = a_dj.insert(arbol_ok)
    print(res_a_insert)
    id_arbol = res_a_insert['data'][0]['id']

    # Actualizamos el árbol cambiando su especie y moviéndolo a otra coordenada válida (106, 106)
    arbol_update = {'id': id_arbol, 'especie': 'Roble_Modificado', 'geom': 'POINT(106 106)'}
    print("\n-> UPDATE (Psycopg) Cambiar especie y mover árbol (Válido):")
    print(a_psy.update(arbol_update))

    # Seleccionamos el árbol para ver si los cambios se guardaron
    print("\n-> SELECT (Django) Leer los datos del árbol modificado:")
    print(a_dj.selectAsDicts({'id': id_arbol}))

    print("\n" + "="*50)
    print(" 3. PRUEBAS DE CAMINOS (LÍNEAS)")
    print("="*50)

    camino_ok = {'nombre': 'Camino_Test', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(100 90, 110 90)'}
    print("-> INSERT (Psycopg) Camino válido:")
    res_c_insert = c_psy.insert(camino_ok)
    print(res_c_insert)
    id_camino = res_c_insert['data'][0]['id']

    # Intentamos cruzarlo con una línea vertical (de 105,85 a 105,95)
    camino_fail = {'id': id_camino, 'nombre': 'Camino_Cruzado', 'geom': 'LINESTRING(105 85, 105 95)'}
    print("\n-> UPDATE (Django) Girar camino para que cruce a sí mismo/otros (DEBE FALLAR):")
    # Como en el update excluimos su propio ID, este debería fallar SOLO si creamos otra línea.
    # Vamos a insertar la cruzada como nueva para forzar el fallo de intersección:
    camino_fail_insert = {'nombre': 'Camino_Cruzado', 'dificultad': 'Media', 'longitud': 10, 'ancho': 2, 'material': 'Grava', 'geom': 'LINESTRING(105 85, 105 95)'}
    print(c_dj.insert(camino_fail_insert))

    print("\n" + "="*50)
    print(" 4. PRUEBAS DE BORRADO (CLEANUP)")
    print("="*50)

    print("-> DELETE (Psycopg) Borrar el Árbol:")
    print(a_psy.delete({'id': id_arbol}))

    print("-> DELETE (Django) Borrar el Camino:")
    print(c_dj.delete({'id': id_camino}))

    print("-> DELETE (Django) Borrar la Zona_Test:")
    print(z_dj.delete({'id': id_zona}))