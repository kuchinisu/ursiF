from django.db import models
import uuid
import os
from apps.user.models import UserAccount
from django.utils import timezone

def path_dir_institucion(instance, filename):
    ext = filename.split('.')[-1]
    nombre_archivo = f"{uuid.uuid4()}.{ext}"
    
    nombre = instance.nombre
    
    ruta_completa = os.path.join('cursos', nombre, 'fotos', nombre_archivo)
    
    print(ruta_completa)  
    
    return ruta_completa


class Institucion(models.Model):
    nombre = models.CharField(max_length=250)
    informacion = models.TextField(blank=True)
    foto = models.ImageField(upload_to=path_dir_institucion)
    
    TIPOS = (
        ('independiente', 'Independiente'),
        ('institucion', 'Institución'),
    )
    
    tipo = models.CharField(default='independiente', choices=TIPOS, max_length=50)
    
    matricula = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if Institucion.objects.all().exists():
            self.matricula = Institucion.objects.all().order_by('matricula').last() + 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    

    @property
    def get_foto(self):
        return self.foto.url if self.foto else ''
    

class Administrativos(models.Model):
    funcion = models.CharField(max_length=255)
    persona = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='persona_administrativa')
    institucion = models.ForeignKey(Institucion, related_name='administrativo_institucion', on_delete=models.CASCADE)

class Alumno(models.Model):
    persona = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='persona_alumno')
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='alumno_institucion')
    matricula_escolar = models.IntegerField(default=1, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_alumno = Alumno.objects.order_by('-matricula_escolar').first()
            self.matricula_escolar = (last_alumno.matricula_escolar + 1) if last_alumno else 1
        super().save(*args, **kwargs)

    @property
    def get_persona(self):
        return self.persona.matricula if self.persona is not None else '' 

class Docente(models.Model):
    persona = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='persona_docente')
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='docente_institucion')

class Asignatura(models.Model):
    nombre = models.CharField(max_length=255)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='asignatura_institucion')
    docentes = models.ManyToManyField(Docente, related_name='asignatura_docente')

class PlanAsignatura(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='plan_asignatura')
    inicio = models.DateTimeField(default=timezone.now)
    final = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'plan de la asignatura: {self.asignatura.nombre} de la institucion {self.asignatura.institucion.nombre}-({self.asignatura.institucion.matricula})'
    
    @property 
    def get_asignatura(self):
        return self.asignatura.nombre if self.asignatura else ''
    

class Actividad(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_de_entrega = models.DateTimeField(default=timezone.now)
    puntos_maximos = models.IntegerField(default=10)
    plan = models.ForeignKey(PlanAsignatura, on_delete=models.CASCADE, related_name='actividad_plan')
    slug = models.SlugField(default=uuid.uuid4, unique=True)

    def get_plan(self):
        return f'plan de la asignatura: {self.plan.asignatura.nombre}' if self.plan is not None else ''
    
class Entrega(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='entrega_alumno')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='entrega_actividad')
    
    ESTADOS = (
        ('calificado', 'Calificado'),
        ('no calificado', 'No Calificado'),
        ('fuera de tiempo', 'Fuera de Tiempo'),
        ('anulado', 'Anulado'),
    )
    
    estado = models.CharField(default='no calificado', choices=ESTADOS, max_length=50)
    puntos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.actividad:
            puntos_max = self.actividad.puntos_maximos
            if self.puntos > puntos_max:
                self.puntos = puntos_max
        super().save(*args, **kwargs)
    def get_alumno (self):
        if self.alumno:
            return self.alumno.matricula_escolar
        else:
            return ''
class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='curso_institucion')
    asignaturas = models.ManyToManyField(Asignatura, related_name='curso_asignaturas')
    alumnos = models.ManyToManyField(Alumno, related_name='curso_alumnos')

    def __str__(self):
        return f'{self.nombre}-{self.institucion.matricula}' if self.institucion is not None else f'{self.nombre}'
    
    @property
    def get_institucion(self):
        return self.institucion.matricula if self.institucion is not None else ''

    