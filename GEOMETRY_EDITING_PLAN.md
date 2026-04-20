# GEOMETRY EDITING PLAN

**Fecha:** 20 de Abril, 2026

## Objetivos
1.  Habilitar `edit: featureGroup` en el Leaflet.Draw para todos los polígonos existentes de la DB.
2.  Transmitir los cambios estructurales post-save (Vertices and Node Dragging) hacia el Backend usando el Framework AJAX `PUT`.
3.  Respetar y actuar sobre los rechazos 400 Bad Request provocados por colisiones en Base de Datos restaurando el Front-end al estado limpio (Rollback Visual).

## Modificaciones Estructurales (Frontend Javascript)
-   Desuso de `zonasLayer`, `caminosLayer` separados e implementación unificada de `editableLayers` (Para respetar abstracción pura de L.Draw).
-   Traducción visual de L.geoJSON a geometrías vectoriales primarias para garantizar su reactividad en Leaflet Toolbars.
-   Manejar `draw:edited` emitiendo iteraciones Fetch con `{ geom: '...' }` como payload sin requerir abrir Modales en UI de metadatos, agilizando el Update Posicional.

Este plan respeta la modularidad Backend que originalmente programó el Cliente en Python (usando de forma segura `.get()`, e `if 'geom'` partial updates).
