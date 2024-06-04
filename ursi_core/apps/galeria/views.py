from csv import excel
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
from apps.utils.error import (
    ArchivoSaveError, CarpetaSlugNotFoundError, CarpetasSerializacionError, DataRetrievalError, GetDataError, GetUserError, 
    ImageSaveError, VideoSaveError,
    CarpetasNotFoundError, ImagenesNotFoundError,
    VideosNotFoundError, ArchivosNotFoundError,
    )

#carpetas
class CarpetasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user

        carpetas = Carpeta.objects.filter(usuario=user, ubicacion='')
        
        if carpetas.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(carpetas, request)
            serializer = CarpetaSerializer(results, many=True)
            
            return paginator.get_paginated_response({'carpetas':serializer.data})
        else:
            return Response({'error':'no hay carpetas para mostrar'}, status=status.HTTP_404_NOT_FOUND)

class CarpetaSlugView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug, format=None):
        user = request.user
        print(f'carpeta por buscar {slug}')
        
        
        try:
            try:
                carpeta = get_object_or_404(Carpeta, slug=slug)
            except Exception as e:
                raise  CarpetaSlugNotFoundError(f'error al intentar obtener la carpeta con el slug {slug}: {e}')
            
            if carpeta.publica or user == carpeta.usuario:

                if carpeta.ubicacion:
                    ubicacion = carpeta.ubicacion + '/' + carpeta.nombre
                else:
                    ubicacion = '/' + carpeta.nombre
                ubicacion = ubicacion.replace('--','/')
                print(f'ubicacion a buscat: {ubicacion}')
                try:
                    carpetas = Carpeta.objects.filter(usuario=user, ubicacion=ubicacion)
                except Exception as e:
                    raise CarpetasNotFoundError(f'error al intentar obtener las carpetas en la ubicacion {ubicacion}: {e}')
                
                if carpetas.exists():
                    
                    try:
                        paginator = LargeSetPagination()
                        results = paginator.paginate_queryset(carpetas, request)
                        serializer = CarpetaSerializer(results, many=True)
                        
                        return paginator.get_paginated_response({'subcarpetas':serializer.data})
                    except Exception as e:
                        raise CarpetasSerializacionError(f'error en la serializacion de las carpetas: {e}')
                else:
                    return Response({'error':'no hay carpetas dentro de la carpeta'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error':'no tienes permiso para acceder a esta carpeta, la carpeta debe ser publica o tu debes ser el dueño de la carpeta'}, status=status.HTTP_401_UNAUTHORIZED)
        except CarpetasNotFoundError as e:
            return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)
        except CarpetaSlugNotFoundError as e:
            return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':f'algo salio mal: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CrearCarpeta(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        pass
    
    def post(self, request, format=None):
        usuario = request.user
        data = request.data

        nombre = data.get('nombre')
        #publica = data.get('publica')
        #ubicacion = data.get('ubicacion')
        #accesible_para = data.get('accesible_para')

        nueva_carpeta = Carpeta(
            nombre = nombre,
            usuario = usuario,
        )

        nueva_carpeta.save()

        return Response({'mensaje':'nueva carpeta creada correctamente'}, status=status.HTTP_201_CREATED)
    

class CrearSubCarpeta(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        pass
    
    def post(self, request, format=None):
        usuario = request.user
        data = request.data

        nombre = data.get('nombre')
        #publica = data.get('publica')
        ubicacion = data.get('ubicacion')
       
        ubicacion = ubicacion.replace('--','')
        
        #accesible_para = data.get('accesible_para')

        nueva_carpeta = Carpeta(
            nombre = nombre,
            usuario = usuario,
            ubicacion = ubicacion,
        )

        nueva_carpeta.save()

        return Response({'mensaje':'nueva subcarpeta creada correctamente'}, status=status.HTTP_201_CREATED)
    
class EditarPrivasidadCarpeta(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, format=None):
        usuario = request.user

        carpeta = get_object_or_404(Carpeta, slug = slug, usuario = usuario)

        carpeta.publica = not carpeta.publica
        carpeta.save()
        
        return Response({'mensaje':'privasidad de la carpeta cambiada con exito'}, status=status.HTTP_200_OK)
    
        
class GetPrivasidadCarpeta(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug, format=None):
        usuario = request.user
        carpeta = get_object_or_404(Carpeta, slug=slug)
        publica = carpeta.publica

        return Response({'publica':publica}, status=status.HTTP_200_OK)
    
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
        print('ete sech')
        try:


            try:
                #usuario
                user = request.user
            except Exception as e:
                raise GetUserError(f'error al intentar obtener el usuario: {e}')
            


            try:
                data = request.data
            except Exception as e:
                raise GetDataError(f'error intentando obtener el request.data: {e}')
            

            try:
                nombre = data.get('nombre')
                carpeta_slug = data.get('carpeta')

                if 'archivo' not in request.FILES:
                    return Response({'error': 'Imagen no encontrada en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

                imagen = request.FILES['archivo']
 
                print('------------------------------------------')
                print('informacion mandada para subir imagen')
                print(f'|nombre| \n {nombre} \n\n |carpeta slug| \n {carpeta_slug} \n\n |imagen| \{imagen}')
                print('---------------------------------------------')
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

                return Response({'mensaje': 'Imagen subida exitosamente'}, status=status.HTTP_201_CREATED)


            except Exception as err:
                raise ImageSaveError(f'Error intentando guardar la imagen: {err}')




        except DataRetrievalError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ImageSaveError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except GetUserError as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except GetDataError as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                
                if 'archivo' not in request.FILES:
                    return Response({'error': 'video no encontrado en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

                video = request.FILES['archivo']
                carpeta = get_object_or_404(Carpeta, slug=carpeta_slug)
            except Exception as err:
                raise DataRetrievalError(f'Error intentando obtener los datos: {err}')

            try:
                nuevo_video = Video(
                    nombre=nombre,
                    carpeta=carpeta,
                )

                nuevo_video.video = video
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

            return paginator.get_paginated_response({'archivos':serializer.data})
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
                )

                nuevo_archivo.archivo = archivo
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
