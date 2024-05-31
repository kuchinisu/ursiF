from os import error
import stat
from tkinter import Image
from uu import Error
from django.shortcuts import render, get_object_or_404
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from urllib3 import Retry
from apps.utils.pagination import LargeSetPagination
from django.utils import timezone

from .serializers import (
    CarpetaSerializer, ImagenSerializer, 
    VideoSerializer, ArchivoSerializer
)
from .models import (
    Carpeta, Imagen, Video, Archivo
)
from apps.utils.pagination import (
    SmallSetPagination, 
    LargeSetPagination, 
    MediumSetPagination
    )
from apps.utils.error import ArchivoSaveError, DataRetrievalError, ImageSaveError, VideoSaveError

#carpetas
class CarpetasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user

        carpetas = Carpeta.objects.filter(usuario=user)
        
        if carpetas.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(carpetas, request)
            serializer = CarpetaSerializer(results, many=True)
            
            return paginator.get_paginated_response({'carpetas':serializer.data})
        else:
            return Response({'error':'no hay carpetas para mostrar'}, status=status.HTTP_404_NOT_FOUND)

class CrearCarpeta(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        pass
    
    def post(self, request, format=None):
        usuario = request.user
        data = request.data

        nombre = data.get('nombre')
        publica = data.get('publica')
        ubicacion = data.get('ubicacion')
        accesible_para = data.get('accesible_para')

        nueva_carpeta = Carpeta(
            nombre = nombre,
            usuario = usuario,
            publica = publica,
            ubicacion = ubicacion,
            accesible_para = accesible_para,
        )

        nueva_carpeta.save()

        return Response({'mensaje':'nueva carpeta creada correctamente'}, status=status.HTTP_201_CREATED)
    
#imagenes

class ImagenesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, carpeta_slug, format=None):
        user = request.user
        carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)

        imagenes = Imagen.objects.filter(carpeta=carpeta)
        if imagenes.exists():
            paginator = LargeSetPagination()

            results = paginator.paginate_queryset(imagenes, request)
            serializer = ImagenSerializer(results, many=True)

            return paginator.get_paginated_response({'imagenes':serializer.data})
        else:
            return Response({'error':'no hay imagenes para mostrar'}, status=status.HTTP_404_NOT_FOUND)
        
class SubirImagen(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        try:
            user = request.user
            data = request.data

            try:
                nombre = data.get('nombre')
                carpeta_slug = data.get('carpeta')
                
                if 'imagen' not in request.FILES:
                    return Response({'error': 'Imagen no encontrada en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

                imagen = request.FILES['imagen']
                carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)
            except Exception as err:
                raise DataRetrievalError(f'Error intentando obtener los datos: {err}')

            try:
                nueva_imagen = Imagen(
                    nombre=nombre,
                    carpeta=carpeta,
                    imagen=imagen
                )
                nueva_imagen.save()
            except Exception as err:
                raise ImageSaveError(f'Error intentando guardar la imagen: {err}')

            return Response({'mensaje': 'Imagen subida exitosamente'}, status=status.HTTP_201_CREATED)

        except DataRetrievalError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except ImageSaveError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({'error': f'A ocurrido un error en la operación: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#videos   
class VideosView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, carpeta_slug, format=None):
        user = request.user
        carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)

        videos = Video.objects.filter(carpeta=carpeta)
        if videos.exists():
            paginator = LargeSetPagination()

            results = paginator.paginate_queryset(videos, request)
            serializer = VideoSerializer(results, many=True)

            return paginator.get_paginated_response({'videos':serializer.data})
        else:
            return Response({'error':'no hay videos para mostrar'}, status=status.HTTP_404_NOT_FOUND)

       
class SubirVideo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        try:
            user = request.user
            data = request.data

            try:
                nombre = data.get('nombre')
                carpeta_slug = data.get('carpeta')
                
                if 'video' not in request.FILES:
                    return Response({'error': 'video no encontrado en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

                video = request.FILES['video']
                carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)
            except Exception as err:
                raise DataRetrievalError(f'Error intentando obtener los datos: {err}')

            try:
                nuevo_video = Video(
                    nombre=nombre,
                    carpeta=carpeta,
                    imagen=video
                )
                nuevo_video.save()
            except Exception as err:
                raise VideoSaveError(f'Error intentando guardar el video: {err}')

            return Response({'mensaje': 'Video subido exitosamente'}, status=status.HTTP_201_CREATED)

        except DataRetrievalError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except VideoSaveError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({'error': f'A ocurrido un error en la operación: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#archivos   
class ArchivosView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, carpeta_slug, format=None):
        user = request.user
        carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)

        archivos = Archivo.objects.filter(carpeta=carpeta)
        if archivos.exists():
            paginator = LargeSetPagination()

            results = paginator.paginate_queryset(archivos, request)
            serializer = ArchivoSerializer(results, many=True)

            return paginator.get_paginated_response({'videos':serializer.data})
        else:
            return Response({'error':'no hay videos para mostrar'}, status=status.HTTP_404_NOT_FOUND)

       
class SubirArchivo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        try:
            user = request.user
            data = request.data

            try:
                nombre = data.get('nombre')
                carpeta_slug = data.get('carpeta')
                
                if 'archivo' not in request.FILES:
                    return Response({'error': 'archivo no encontrado en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

                archivo = request.FILES['archivo']
                carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)
            except Exception as err:
                raise DataRetrievalError(f'Error intentando obtener los datos: {err}')

            try:
                nuevo_archivo = Archivo(
                    nombre=nombre,
                    carpeta=carpeta,
                    imagen=archivo
                )
                nuevo_archivo.save()

            except Exception as err:
                raise ArchivoSaveError(f'Error intentando guardar el archivo: {err}')

            return Response({'mensaje': 'Video subido exitosamente'}, status=status.HTTP_201_CREATED)

        except DataRetrievalError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except ArchivoSaveError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({'error': f'A ocurrido un error en la operación: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
