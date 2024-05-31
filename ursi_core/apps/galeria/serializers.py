from rest_framework import serializers
from .models import Carpeta, Imagen, Video, Archivo

class CarpetaSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='get_disciplina')(source='get_usuario')

    class Meta:
        model=Carpeta
        fields = [
            'nombre',
            'usuario',
            'publica',
            'ubicacion',
            'slug',
            'accesible_para',
        ]

class ImagenSerializer(serializers.ModelSerializer):
    imagen = serializers.CharField(source='get_imagen')

    class Meta:
        model=Imagen
        fields = [
            'nombre',
            'imagen',
            'tags',
            'carpeta',

        ]


class VideoSerializer(serializers.ModelSerializer):
   video = serializers.CharField(source='get_video')

   class Meta:
        model = Video
        fields = [
            'nombre',
            'video',
            'tags',
            'carpeta',
        ]

class ArchivoSerializer(serializers.ModelSerializer):
    archivo = serializers.CharField(source='get_archivo')
    class Meta:
        model = Archivo
        fields = [
            'nombre',
            'archivo',
            'tags',
            'carpeta',

        ]