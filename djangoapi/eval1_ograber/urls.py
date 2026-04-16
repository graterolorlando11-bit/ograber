from django.urls import path, include
from rest_framework.routers import DefaultRouter
from eval1_ograber import views

router = DefaultRouter()
router.register(r'zonas', views.ZonaViewSet)
router.register(r'caminos', views.CaminoViewSet)
router.register(r'arboles', views.ArbolViewSet)

urlpatterns = [
    # APIs REST
    path('', include(router.urls)),

    # Vistas web
    path('mapa/', views.mapa_principal, name='mapa'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('logs/', views.mis_logs, name='mis_logs'),
    path('datos-geo/', views.obtener_datos_geo, name='datos_geo'),
]