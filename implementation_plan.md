# Diagnóstico y Plan de Refactorización

## Contexto y Diagnóstico
Tras analizar tus scripts en la carpeta `djangoapi/scripts/eval1`, mi **diagnóstico** refleja que tienes toda la razón:
1. **Tu lógica original:** Habías programado módulos completos (`ZonasDjango`, `ArbolesDjango`, `CaminosDjango`) que gestionan toda la lógica de Inserción, Actualización y Borrado. Ellos aplican el *SnapToGrid* y las validaciones espaciales (`geom__contains`, etc.), y devuelven respuestas formateadas (`{'ok': True, 'message': ...}`).
2. **Lo que hizo el agente anterior:** En lugar de importar tus clases y usarlas como el "motor" del backend, el agente optó por la forma estándar —pero invasiva— de *Django Rest Framework* (DRF). Ignoró tus scripts y **copió** las validaciones de superposición e intersección directamente dentro de los métodos `create` y `update` de `eval1_ograber/serializers.py`.
3. **El Fix no portado:** El otro agente notó que usar `geom__relate=(g, 'T********')` para detectar si una Zona se superponía con otra daba falsos positivos cuando compartían un borde, así que lo reemplazó por una consulta pura de PostGIS usando `ST_Overlaps`. ¡Pero hizo ese arreglo en los serializers y nunca lo llevó a tu script `zonas_django.py`!

## User Review Required

> [!WARNING]
> Cambiar la arquitectura de los `Serializers` nativos a invocaciones de tus scripts romperá temporalmente las operaciones estándar del API hasta que adaptemos las Vistas (`eval1_ograber/views.py`) para consumir la estructura `{'ok': ..., 'data': ...}` que devuelven tus funciones. ¿Estás de acuerdo con este enfoque para priorizar el uso de tu propio código base?

## Proposed Changes

### Refactorización de Capa Lógica (`scripts/eval1`)
Actualizaremos tus funciones para mantener las mejoras necesarias de postgis resolviendo falsos positivos:
#### [MODIFY] `djangoapi/scripts/eval1/zonas/zonas_django.py`
  - Reemplazar la validación `geom__relate` por la verificación nativa a nivel de Base de Datos vía `ST_Overlaps` para evitar el bug de las zonas adyacentes.

### Modificación de la API (Serializers y Vistas)
Para que DRF no cree dependencias autónomas y dependa exclusivamente de tu lógica empotrada en `scripts`, adaptaremos el flujo de los Endpoints:
#### [MODIFY] `djangoapi/eval1_ograber/serializers.py`
  - Limpiaremos todos los métodos `create` y `update` que contienen las consultas geográficas quemadas ("hardcoded"). Retomaremos la declaración simple de metadatos.
#### [MODIFY] `djangoapi/eval1_ograber/views.py`
  - Sobreescribiremos los métodos del ciclo de vida en `ZonaViewSet`, `CaminoViewSet` y `ArbolViewSet` (`create`, `update`, `destroy`).
  - Estos métodos instanciarán directamente `ZonasDjango()`, `ArbolesDjango()` y `CaminosDjango()` y ejecutarán el envío de diccionarios, usando su respuesta para resolver al cliente.

## Open Questions

> [!IMPORTANT]
> Tus scripts asumen que siempre llegará toda la estructura del diccionario `d` a actualizar e insertar y a partir de allí generan una instancia o error manualmente. ¿Deseas que al hacer esto ignoremos las pre-validaciones convencionales de DRF y deleguemos **todo** directamente a tu método `insert(d)` y `update(d)`?

## Verification Plan

### Test de Conexión (El chequeo que pediste)
Antes de romper o cambiar ninguna funcionalidad actual, nos conectaremos al contenedor:
- Ejecutaremos pruebas locales probando que el contenedor de `postgis` y `djangoapi` funcionan perfecto. Hemos comprobado la salud de los contenedores (`docker-compose ps` reporta que todos los puertos están arriba funcionando: puertos 8001, 8080 y 8432).

### Automated Tests
- Validar todo con tu actual `eval1_ograber/tests.py` corriendo `docker-compose exec djangoapi python manage.py test eval1_ograber` y el archivo `test_completo.py`.
