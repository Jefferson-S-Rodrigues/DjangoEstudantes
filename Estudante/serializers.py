from rest_framework import serializers
from .models import Estudante, Cursando, Curso

class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Curso
        fields = '__all__'

class EstudanteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estudante
        fields = '__all__'

class CursandoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cursando
        fields = '__all__'