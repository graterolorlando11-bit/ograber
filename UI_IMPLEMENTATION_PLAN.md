# Frontend UI Implementation Log

**Fecha de Inicio**: 20 de Abril, 2026

## Objetivos Generales
Desarrollar el Front-End (Vistas Web HTML/CSS/JS) para interactuar armónicamente con la API Geoespacial que hemos finalizado, priorizando un diseño limpio, moderno (Rich Aesthetics) y cubriendo las 4 operaciones (CRUD: Insert, Select, Update, Delete) nativas de la web app.

## Estructura Planificada

### 1. Vistas de Autenticación Modernizadas
- **Problema actual**: El Login está alojado como un "string HTML gigantesco" incrustado en el propio archivo Python `views.py`. Además, falta registrar nuevos usuarios.
- **Solución**: Crearemos carpetas reales `templates/core/`. Construiremos allí `login.html` y `registro.html`.
- **Estrategia para Roles**: El UI incluirá un campo especial oculto en el registro: la "Clave Maestra de Admin". Si un estudiante introduce una clave (ej. `SuperMap24`) al registrarse, el backend creará el usuario con el permiso flag `is_staff = True`. Esto distinguirá quién puede rayar el mapa y quién solo es un invitado.

### 2. Panel del Mapa Interactivo (CRUD Spatial)
El archivo `mapa.html` será elevado hacia una aplicación single-page a nivel del script de Javascript usando Fetch API interactuando con nuestros módulos ya listos:

- **SELECT**: Cargar todos los elementos (Ya implementado medianamente). Aplicaremos **Glassmorphism CSS** (paneles translúcidos tipo vidrio) para una previsualización espectacular de la información cuando se clickea un polígono/árbol.
- **INSERT**: Añadir soporte de la librería **Leaflet Draw** (los clásicos botones de dibujar polígono, línea y colocar marcador). Cuando el *Admin* dibuje uno y haga doble click, brincará un pop-up HTML pidiéndole el resto de datos faltantes (Especie si es un arbol; Nombre, Dificultad si es un camino). Javascript enviará la petición POST a `/eval1_ograber/arboles/`.
- **UPDATE y DELETE**: Cuando un *Admin* seleccione un objeto del mapa, el panel acrílico lateral le habilitará los botones ocultos ("Actualizar Valores" o "Borrar"). 

## Reglas de Interfaz (Design System)
- Todo funcionará sobre paletas de colores coherentes en lugar de colores Bootstrap rústicos. (Se sugiere fuentes como Inter o Roboto y contrastes sutiles con sombras).
- Solo los usuarios `is_staff` podrán visualizar las barras de herramientas de edición de nodos y eliminación de registros. Todos disfrutarán de las consultas e interrogación de info.
