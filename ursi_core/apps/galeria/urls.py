from django.urls import path

from apps.galeria.views import (
    ArchivosView, CarpetasView, 
    CrearCarpeta, ImagenesView, 
    SubirArchivo, SubirImagen, 
    SubirVideo, VideosView,
    )

urlpatterns = [
    path('lista/carpetas/', CarpetasView.as_view()),
    path('lista/imagenes/', ImagenesView.as_view()),
    path('lista/videos/', VideosView.as_view()),
    path('lista/archivos/', ArchivosView.as_view()),

    path('crear/carpeta/', CrearCarpeta.as_view()),
    path('subir/imagen/', SubirImagen.as_view()),
    path('subir/video/', SubirVideo.as_view()),
    path('subir/archivo/', SubirArchivo.as_view()),
]
