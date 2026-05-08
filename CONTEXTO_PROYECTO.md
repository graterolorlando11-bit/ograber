# Contexto General del Proyecto: Portal GEO (ograber)

Este documento sirve como un resumen técnico y bitácora del estado actual del proyecto, la arquitectura, y las decisiones críticas que hemos tomado a lo largo del desarrollo y el despliegue en la VPS.

## 1. Arquitectura y Stack Tecnológico
*   **Frontend:** HTML5, CSS (Bootstrap 5), JavaScript puro.
*   **Mapa Interactivo:** Leaflet.js junto con Leaflet.Draw para la edición y creación de geometrías espaciales. Trabaja nativamente con el sistema de coordenadas **WGS84 (EPSG:4326)**.
*   **Backend:** Django con GeoDjango (Python). Provee tanto las vistas web clásicas como una API REST (vía Django REST Framework).
*   **Base de Datos:** PostgreSQL con la extensión espacial PostGIS.
*   **Despliegue (Producción/VPS):** Contenedores gestionados por Docker (`docker compose`). La aplicación está servida detrás de un proxy reverso (Nginx/Apache) que inyecta el prefijo `/api/` en la URL de producción (`https://graterol.geomaticaupv.es/api/`).

## 2. Bases de Datos y Geometría Espacial
La gestión de los sistemas de referencia de coordenadas (SRID) es uno de los pilares más complejos de este proyecto.

*   **Esquema de Almacenamiento:** Las tablas (`zonas`, `caminos`, `arboles`) guardan sus geometrías con **SRID 25830 (UTM Huso 30N)** según el modelo de Django.
*   **Recepción Frontend:** Leaflet dibuja y envía geometrías en grados decimales (EPSG: 4326).
*   **Lógica Backend (El "Hack" Geométrico):**
    *   Al recibir un GeoJSON desde el frontend, pasa por un `ST_SnapToGrid` asumiendo grados.
    *   Para poder **calcular el área o la longitud en metros reales**, la geometría original pura (`g.wkt`) es convertida en memoria a EPSG 4326 y luego transformada a EPSG 25830 (`.transform(25830)`).
    *   Esto garantiza que los campos métricos (Área, Perímetro, Longitud) queden guardados matemáticamente exactos.
    *   El error `Input geometry already has SRID: 25830` fue solventado asegurándonos de pasarle texto puro WKT a Django antes de asignar el SRID, evadiendo las firmas binarias incrustadas por PostGIS.

## 3. Seguridad y Atributos (Blindaje)
Para asegurar la calidad e integridad de los datos en base de datos:
*   **Inputs Deshabilitados (Readonly):** Las casillas de dimensiones (área, longitud, etc.) fueron bloqueadas en `mapa.html`. El frontend dejó de ser la fuente de verdad. El backend ahora calcula imperativamente y guarda estos datos.
*   **Dominios (Combobox):** Los campos de texto abierto propensos a errores tipográficos se cambiaron por `<select>` cerrados. 
    *   Ej: *Estado de árbol (Sano, Regular, Decadente, Muerto)*, *Tipo de Zona*, *Dificultad de Camino*.

## 4. Auditoría Inteligente (`perfil.html`)
El sistema de logs cuenta con un "Inspector Espacial" modal:
*   Al abrir el registro de creación (`CREATE`), el mapa "Antes" desaparece dinámicamente y el mapa "Después" asume todo el ancho en verde.
*   En eliminación (`DELETE`), el "Antes" toma el control en rojo y el "Después" se oculta.
*   En edición (`UPDATE`), ambos se muestran para comparar el cambio.

## 5. Ruteo Dinámico de URLs (Problema del Proxy)
La migración de local (`localhost:8000/`) a la VPS (`https://graterol.../api/`) rompió los botones y scripts.
*   **Solución en Plantillas y Vistas:** Se erradicaron las rutas fijas (`/eval1_ograber/...`). En su lugar se utilizan Template Tags nativas de Django (`{% url 'nombre_vista' %}`) y la función `redirect('nombre_vista')` en Python. Esto permite que Django adapte dinámicamente la ruta, sabiendo automáticamente que existe el prefijo `/api/`.
*   **Solución JS / Fetch API:** Los llamados a la API de Django REST (`/eval1_ograber/endpoint/`) en `mapa.html` se cambiaron a rutas relativas (`../endpoint/`) o inyecciones de `{% url %}`, haciendo el frontend proxy-agnostic.

## 6. Despliegue en VPS (Comandos Críticos)
El repositorio clonado en el servidor remoto utiliza el contenedor de desarrollo asilado para evitar colisiones con bases de datos compartidas.
*   La configuración vive en los archivos `.env` y `.env.dev` que fueron rastreados (tracked) y subidos vía Git porque el `.gitignore` solo omitía a `.env.prod`.
*   **Base de Datos actual:** `graterol`.
*   **Token Admin:** `SuperMap24`.

**Flujo estándar para actualizar la API en vivo:**
1. Hacer un `git push` en local.
2. Hacer SSH al VPS y entrar a la carpeta: `cd ~/docker/gescont/ograber`
3. Traer los cambios: `git pull origin main`
4. Reconstruir e iniciar servicios: `docker compose up -d --build`
5. (Solo si hubieron cambios en la estructura de DB):
   `docker compose exec djangoapi python manage.py makemigrations`
   `docker compose exec djangoapi python manage.py migrate`

---
*Documento autogenerado por Antigravity (IA) como bitácora de la arquitectura consolidada.*
