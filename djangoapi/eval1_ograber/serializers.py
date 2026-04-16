from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from eval1_ograber.models import Zona, Camino, Arbol

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'

    def create(self, validated_data):
        # Snap to grid
        snap_grid = 0.0001
        cur = connection.cursor()
        cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [validated_data['geom'].wkt, snap_grid])
        geom_snapped = cur.fetchone()[0]
        g = GEOSGeometry(geom_snapped, srid=25830)

        if not g.valid:
            raise serializers.ValidationError('Geometría inválida')

        # Check no overlap - use ST_Overlaps to detect real overlaps (not just touching boundaries)
        cur.execute("SELECT COUNT(*) FROM eval1_ograber_zona WHERE ST_Overlaps(geom, ST_GeomFromText(%s, 25830))", [g.wkt])
        if cur.fetchone()[0] > 0:
            raise serializers.ValidationError('La zona se superpone con otra existente')

        validated_data['geom'] = g
        return super().create(validated_data)

    def update(self, instance, validated_data):
        snap_grid = 0.0001
        if 'geom' in validated_data:
            cur = connection.cursor()
            cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [validated_data['geom'].wkt, snap_grid])
            g = GEOSGeometry(cur.fetchone()[0], srid=25830)

            if not g.valid:
                raise serializers.ValidationError('Geometría inválida')

            # Check no overlap excluding self
            cur.execute("SELECT COUNT(*) FROM eval1_ograber_zona WHERE id != %s AND ST_Overlaps(geom, ST_GeomFromText(%s, 25830))", [instance.id, g.wkt])
            if cur.fetchone()[0] > 0:
                raise serializers.ValidationError('La zona se superpone con otra existente')

            validated_data['geom'] = g

        return super().update(instance, validated_data)

class CaminoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camino
        fields = '__all__'

    def create(self, validated_data):
        snap_grid = 0.0001
        cur = connection.cursor()
        cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [validated_data['geom'].wkt, snap_grid])
        geom_snapped = cur.fetchone()[0]
        g = GEOSGeometry(geom_snapped, srid=25830)

        if not g.valid:
            raise serializers.ValidationError('Geometría inválida')

        # Check no intersection
        if Camino.objects.filter(geom__intersects=g).exists():
            raise serializers.ValidationError('El camino se cruza con otro existente')

        validated_data['geom'] = g
        return super().create(validated_data)

    def update(self, instance, validated_data):
        snap_grid = 0.0001
        if 'geom' in validated_data:
            cur = connection.cursor()
            cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [validated_data['geom'].wkt, snap_grid])
            g = GEOSGeometry(cur.fetchone()[0], srid=25830)

            if not g.valid:
                raise serializers.ValidationError('Geometría inválida')

            # Check no intersection excluding self
            if Camino.objects.filter(geom__intersects=g).exclude(id=instance.id).exists():
                raise serializers.ValidationError('El camino se cruza con otro existente')

            validated_data['geom'] = g

        return super().update(instance, validated_data)

class ArbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arbol
        fields = '__all__'

    def create(self, validated_data):
        snap_grid = 0.0001
        cur = connection.cursor()
        cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [validated_data['geom'].wkt, snap_grid])
        geom_snapped = cur.fetchone()[0]
        g = GEOSGeometry(geom_snapped, srid=25830)

        if not g.valid:
            raise serializers.ValidationError('Geometría inválida')

        # Check inside a zone
        if not Zona.objects.filter(geom__contains=g).exists():
            raise serializers.ValidationError('El árbol debe estar dentro de una zona')

        validated_data['geom'] = g
        return super().create(validated_data)

    def update(self, instance, validated_data):
        snap_grid = 0.0001
        if 'geom' in validated_data:
            cur = connection.cursor()
            cur.execute("SELECT ST_SnapToGrid(ST_GeomFromText(%s, 25830), %s)", [validated_data['geom'].wkt, snap_grid])
            g = GEOSGeometry(cur.fetchone()[0], srid=25830)

            if not g.valid:
                raise serializers.ValidationError('Geometría inválida')

            # Check inside a zone
            if not Zona.objects.filter(geom__contains=g).exists():
                raise serializers.ValidationError('El árbol debe estar dentro de una zona')

            validated_data['geom'] = g

        return super().update(instance, validated_data)