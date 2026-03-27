from scripts.eval1.zonas.zonas_django import ZonasDjango
from scripts.eval1.zonas.zonas_psycopg import ZonasPsycopg
from scripts.eval1.caminos.caminos_django import CaminosDjango
from scripts.eval1.caminos.caminos_psycopg import CaminosPsycopg
from scripts.eval1.arboles.arboles_django import ArbolesDjango
from scripts.eval1.arboles.arboles_psycopg import ArbolesPsycopg

def run():
    z_dj = ZonasDjango()
    z_psy = ZonasPsycopg()
    c_dj = CaminosDjango()
    c_psy = CaminosPsycopg()
    a_dj = ArbolesDjango()
    a_psy = ArbolesPsycopg()

    print("\n" + "="*50)
    print(" 1. ZONAS (POLÍGONOS) - REGLA: No superponerse")
    print("="*50)
    
    # # --- DJANGO ---
    # # ÉXITO: Espacio libre (60 a 70)
    # zona_dj_ok = {'nombre': 'ZD_OK', 'tipo': 'A', 'area': 100, 'perimetro': 40, 'responsable': 'Demo', 'geom': 'POLYGON((60 0, 70 0, 70 10, 60 10, 60 0))'}
    # print("ZONA DJANGO (ÉXITO):", z_dj.insert(zona_dj_ok))
    
    # # FALLO: Pisa tu Z1 original (0 a 10)
    # zona_dj_fail = {'nombre': 'ZD_FAIL', 'tipo': 'A', 'area': 100, 'perimetro': 40, 'responsable': 'Demo', 'geom': 'POLYGON((5 5, 15 5, 15 15, 5 15, 5 5))'}
    # print("ZONA DJANGO (FALLO):", z_dj.insert(zona_dj_fail))

    # # --- PSYCOPG ---
    # # ÉXITO: Espacio libre (80 a 90)
    # zona_psy_ok = {'nombre': 'ZP_OK', 'tipo': 'A', 'area': 100, 'perimetro': 40, 'responsable': 'Demo', 'geom': 'POLYGON((80 0, 90 0, 90 10, 80 10, 80 0))'}
    # print("ZONA PSYCOPG (ÉXITO):", z_psy.insert(zona_psy_ok))
    
    # # FALLO: Pisa tu Z2 original (20 a 30)
    # zona_psy_fail = {'nombre': 'ZP_FAIL', 'tipo': 'A', 'area': 100, 'perimetro': 40, 'responsable': 'Demo', 'geom': 'POLYGON((25 5, 35 5, 35 15, 25 15, 25 5))'}
    # print("ZONA PSYCOPG (FALLO):", z_psy.insert(zona_psy_fail))


    # print("\n" + "="*50)
    # print(" 2. ÁRBOLES (PUNTOS) - REGLA: Estar dentro de una zona")
    # print("="*50)
    
    # # --- DJANGO ---
    # # ÉXITO: Cae dentro de la zona ZD_OK que creaste arriba (x=65)
    # arbol_dj_ok = {'especie': 'Pino_DJ', 'altura': 10, 'diametro': 1, 'edad': 5, 'estado': 'Sano', 'geom': 'POINT(65 5)'}
    # print("ÁRBOL DJANGO (ÉXITO):", a_dj.insert(arbol_dj_ok))
    
    # # FALLO: Cae fuera de todo el parque
    # arbol_dj_fail = {'especie': 'Pino_DJ_Malo', 'altura': 10, 'diametro': 1, 'edad': 5, 'estado': 'Sano', 'geom': 'POINT(100 100)'}
    # print("ÁRBOL DJANGO (FALLO):", a_dj.insert(arbol_dj_fail))

    # --- PSYCOPG ---
    # ÉXITO: Cae dentro de la zona ZP_OK que creaste arriba (x=85)
    # arbol_psy_ok = {'especie': 'Pino_PSY', 'altura': 10, 'diametro': 1, 'edad': 5, 'estado': 'Sano', 'geom': 'POINT(85 5)'}
    # print("ÁRBOL PSYCOPG (ÉXITO):", a_psy.insert(arbol_psy_ok))
    
    # # FALLO: Cae fuera de todo el parque
    arbol_psy_fail = {'especie': 'Pino_PSY_Malo', 'altura': 10, 'diametro': 1, 'edad': 5, 'estado': 'Sano', 'geom': 'POINT(200 200)'}
    print("ÁRBOL PSYCOPG (FALLO):", a_psy.insert(arbol_psy_fail))


    # print("\n" + "="*50)
    # print(" 3. CAMINOS (LÍNEAS) - REGLA: No cruzarse entre ellos")
    # print("="*50)
    
    # # --- DJANGO ---
    # # ÉXITO: Línea horizontal aislada abajo del todo (y=-30)
    # camino_dj_ok = {'nombre': 'CD_OK', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(0 -30, 10 -30)'}
    # print("CAMINO DJANGO (ÉXITO):", c_dj.insert(camino_dj_ok))
    
    # # FALLO: Línea vertical que corta a tu C1 (C1 pasa por y=-10)
    # camino_dj_fail = {'nombre': 'CD_FAIL', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(5 -5, 5 -15)'}
    # print("CAMINO DJANGO (FALLO):", c_dj.insert(camino_dj_fail))

    # # --- PSYCOPG ---
    # # ÉXITO: Otra línea horizontal aislada (y=-40)
    # camino_psy_ok = {'nombre': 'CP_OK', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(20 -40, 30 -40)'}
    # print("CAMINO PSYCOPG (ÉXITO):", c_psy.insert(camino_psy_ok))
    
    # # FALLO: Línea vertical que corta a tu C2 (C2 pasa por y=-10)
    # camino_psy_fail = {'nombre': 'CP_FAIL', 'dificultad': 'Fácil', 'longitud': 10, 'ancho': 2, 'material': 'Tierra', 'geom': 'LINESTRING(25 -5, 25 -15)'}
    # print("CAMINO PSYCOPG (FALLO):", c_psy.insert(camino_psy_fail))

    # python manage.py runscript scripts.eval1.test3