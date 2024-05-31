from django.db import models
from apps.tags.models import Tags
import uuid
import os
from apps.user.models import UserAccount
from django.utils.text import slugify

def path_dir(instance, filename):
    ext = filename.split('.')[-1]
    nombre_archivo = f"{uuid.uuid4()}.{ext}"
    
    ubicacion = instance.carpeta.ubicacion or ""
    nombre = instance.nombre
    usuario = f'{instance.usuario.nombre}_{instance.usuario.matricula}'
    carpeta = instance.carpeta.nombre
    ruta_completa = os.path.join(usuario, ubicacion, nombre, carpeta, nombre_archivo)
    
    print(ruta_completa)  
    
    return ruta_completa

class Carpeta(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(UserAccount, related_name='carpeta_usuario', on_delete=models.CASCADE)
    publica = models.BooleanField(default=False)
    ubicacion = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    
    OPCIONES_DE_ACCESIBILIDAD = (
        ('todos', 'todos'),
        ('seleccionados','seleccionados'),
    )

    accesible_para = models.CharField(default='seleccionados', max_length=50, choices=OPCIONES_DE_ACCESIBILIDAD)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_usuario(self):
        if self.usuario:
            return self.usuario.nombre

    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    nombre = models.CharField(max_length=250)
    imagen = models.ImageField(upload_to=path_dir)
    tags = models.ManyToManyField(Tags, related_name='tags_imagen', blank=True)
    carpeta = models.ForeignKey(Carpeta, related_name='imagen_carpeta', on_delete=models.CASCADE)

    @property
    def get_imagen(self):
        return self.imagen.url if self.imagen else ''
    
    def get_carpeta(self):
        if self.carpeta:
            return self.carpeta.slug
        return  ''
class Video(models.Model):
    nombre = models.CharField(max_length=250)
    video = models.FileField(upload_to=path_dir)
    tags = models.ManyToManyField(Tags, related_name='tags_video', blank=True)
    carpeta = models.ForeignKey(Carpeta, related_name='video_carpeta', on_delete=models.CASCADE)

    @property
    def get_video(self):
        return self.video.url if self.video else ''

    def get_carpeta(self):
        if self.carpeta:
            return self.carpeta.slug
        return  ''
class Archivo(models.Model):
    nombre = models.CharField(max_length=250)
    archivo = models.FileField(upload_to=path_dir)
    tags = models.ManyToManyField(Tags, blank=True, related_name='tags_archivo')
    carpeta = models.ForeignKey(Carpeta, related_name='archivo_nombre', on_delete=models.CASCADE)

    @property
    def get_archivo(self):
        return self.archivo.url if self.archivo else ''

    def get_carpeta(self):
        if self.carpeta:
            return self.carpeta.slug
        return  ''