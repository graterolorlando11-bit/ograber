from rest_framework import serializers
from eval1_ograber.models import Zona, Camino, Arbol

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'

class CaminoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camino
        fields = '__all__'

class ArbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arbol
        fields = '__all__'