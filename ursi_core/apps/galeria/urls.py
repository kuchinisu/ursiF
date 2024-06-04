from django.urls import path

from apps.galeria.views import (
    ArchivosView, CarpetaSlugView, CarpetasView, 
    CrearCarpeta, CrearSubCarpeta, EditarAccesoCarpeta, EditarPrivasidadCarpeta, GetPrivasidadCarpeta, ImagenesView, 
    SubirArchivo, SubirImagen, 
    SubirVideo, VideosView, GetAccesoCarpeta
    )

urlpatterns = [
    path('lista/carpetas/', CarpetasView.as_view()),
    path('lista/imagenes/<carpeta_slug>/', ImagenesView.as_view()),
    path('lista/videos/<carpeta_slug>/', VideosView.as_view()),
    path('lista/archivos/<carpeta_slug>/', ArchivosView.as_view()),

    path('carpeta/slug/<slug>/', CarpetaSlugView.as_view()),
   
    path('privacidad/carpeta/slug/<slug>/', GetPrivasidadCarpeta.as_view()),
    path('editar/accesibilidad/carpeta/slug/<slug>/', EditarAccesoCarpeta.as_view()),
    path('get/accesibilidad/carpeta/slug/<slug>/', GetAccesoCarpeta.as_view()),

    path('editar/carpeta/<slug>/', EditarPrivasidadCarpeta.as_view()),

    path('crear/carpeta/', CrearCarpeta.as_view()),
    path('crear/subcarpeta/', CrearSubCarpeta.as_view()),
    path('subir/imagen/', SubirImagen.as_view()),
    path('subir/video/', SubirVideo.as_view()),
    path('subir/archivo/', SubirArchivo.as_view()),
]
