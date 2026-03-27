from django.contrib.gis.db import models

class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    perimetro = models.FloatField(null=True, blank=True)
    responsable = models.CharField(max_length=100, null=True, blank=True)
    geom = models.PolygonField(srid=25830)

    class Meta:
        managed = False # Le dice a Django que la tabla ya esta
        db_table = 'zonas' # El nombre exacto de tu tabla en PostGIS

class Camino(models.Model):
    nombre = models.CharField(max_length=100)
    dificultad = models.CharField(max_length=50, null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    ancho = models.FloatField(null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    geom = models.LineStringField(srid=25830)

    class Meta:
        managed = False
        db_table = 'caminos'

class Arbol(models.Model):
    especie = models.CharField(max_length=100)
    altura = models.FloatField(null=True, blank=True)
    diametro = models.FloatField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    geom = models.PointField(srid=25830)

    class Meta:
        managed = False
        db_table = 'arboles'