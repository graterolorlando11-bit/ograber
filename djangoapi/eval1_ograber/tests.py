from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from knox.models import AuthToken
from eval1_ograber.models import Zona, Camino, Arbol

class ZonaValidationTest(APITestCase):
    def setUp(self):
        # Crear usuario de test con permisos de staff
        self.user = User.objects.create_user(username='testuser', password='testpass', is_staff=True)

        # Crear token de autenticación
        instance, token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Crear zona de prueba
        geom = GEOSGeometry('POLYGON ((-0.4 39.4, -0.3 39.4, -0.3 39.5, -0.4 39.5, -0.4 39.4))', srid=25830)
        self.zona = Zona.objects.create(nombre='Zona Test', geom=geom)

    def test_zona_no_overlap_create(self):
        """Test que no se permite crear zonas que se superponen"""
        # Intentar crear una zona que se superpone
        data = {
            'nombre': 'Zona Superpuesta',
            'geom': 'POLYGON ((-0.35 39.45, -0.25 39.45, -0.25 39.55, -0.35 39.55, -0.35 39.45))'
        }

        response = self.client.post('/eval1_ograber/zonas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('superpone', str(response.data))

    def test_zona_no_overlap_update(self):
        """Test que no se permite actualizar zonas para que se superponen"""
        # Crear segunda zona
        geom2 = GEOSGeometry('POLYGON ((-0.2 39.4, -0.1 39.4, -0.1 39.5, -0.2 39.5, -0.2 39.4))', srid=25830)
        zona2 = Zona.objects.create(nombre='Zona Test 2', geom=geom2)

        # Intentar actualizar zona2 para que se superponga con zona1
        data = {
            'nombre': 'Zona Test 2 Actualizada',
            'geom': 'POLYGON ((-0.35 39.45, -0.25 39.45, -0.25 39.55, -0.35 39.55, -0.35 39.45))'
        }

        response = self.client.put(f'/eval1_ograber/zonas/{zona2.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('superpone', str(response.data))

class ArbolValidationTest(APITestCase):
    def setUp(self):
        # Crear usuario de test con permisos de staff
        self.user = User.objects.create_user(username='testuser2', password='testpass', is_staff=True)

        # Crear token de autenticación
        instance, token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Crear zona que contenga el árbol
        geom = GEOSGeometry('POLYGON ((-0.4 39.4, -0.3 39.4, -0.3 39.5, -0.4 39.5, -0.4 39.4))', srid=25830)
        self.zona = Zona.objects.create(nombre='Zona Test', geom=geom)

    def test_arbol_inside_zona(self):
        """Test que los árboles deben estar dentro de una zona"""
        # Crear árbol dentro de la zona
        data = {
            'especie': 'Pino Test',
            'geom': 'POINT (-0.35 39.45)'
        }

        response = self.client.post('/eval1_ograber/arboles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_arbol_outside_zona_fails(self):
        """Test que falla si el árbol está fuera de cualquier zona"""
        # Intentar crear árbol fuera de la zona
        data = {
            'especie': 'Roble Fuera',
            'geom': 'POINT (-0.1 39.45)'  # Fuera de la zona
        }

        response = self.client.post('/eval1_ograber/arboles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('fuera de las zonas', str(response.data))