# PROFILE IMPLEMENTATION PLAN

**Fecha:** 20 de Abril, 2026

## Requerimientos Levantados
1.  **Bugfix Autenticación API:** El `FETCH` de javascript en `mapa.html` está sufriendo bloqueos `401 Unauthorized`. La API DRF ignora las Cookies de inicio de sesión web debido a que `DEFAULT_AUTHENTICATION_CLASSES` en `settings.py` fue sustituido íntegramente por `TokenAuthentication`. Solución: Restaurar `SessionAuthentication` al array global.
2.  **Tracking y Audit (Mis Logs):** Se requiere que todo evento (Crear, Editar, Borrar, e Inspección en masa) arroje una estela perenne en la base de datos para registrar el comportamiento (¿Quién movió el árbol?). El modelo `UserActionLog` será poblado dinámicamente desde `eval1_ograber/views.py`.
3.  **Gestión de Cuentas Web:** Una pestaña nueva (Dashboard Personal) servirá como el panel consolidado de configuración para un usuario.

## Componentes a Modificar
- **`djangoapi/djangoapi/settings.py`**: Solucionar bloqueos de lectura/escritura AJAX añadiendo `rest_framework.authentication.SessionAuthentication`.
- **`core/urls.py`**: Anexar `path('perfil/', views.ProfileView.as_view(), name='core_profile')`.
- **`core/views.py`**: Escribir la controladora `ProfileView` capaz de digerir: Cambio de alias (evitando redundancias en BD), Cambio de password encriptado, Destrucción de la entidad del usuario.
- **`core/templates/core/perfil.html`**: Presentación basada en cristales gráficos (Glassmorphism), reuniendo los formularios y el Timeline de historial extraído localmente para cada usuario.
