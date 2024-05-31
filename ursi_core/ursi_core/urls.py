from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

    path('galeria/' , include('apps.galeria.urls')),
    path('cursos/' , include('apps.curso.urls')),

    path('admin/', admin.site.urls),
]
