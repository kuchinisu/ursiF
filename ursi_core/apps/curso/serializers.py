from rest_framework import serializers

from ursi_core.apps.curso.models import (
    Actividad, Administrativos, 
    Alumno, Asignatura, Docente, Institucion
    )

class InstitucionSerializer(serializers.ModelSerializer):
    foto = serializers.CharField(source='get_foto')
    class Meta:
        model = Institucion
        fields = [
            'nombre',
            'informacion',
            'foto',
            'tipo',
        ]

class AdministrativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrativos
        fields = [
            'funcion',
            'persona',
            'institucion',
        ]

class AlumnoSerializer(serializers.ModelSerializer):
    persona = serializers.CharField(source='get_persona')
    class Meta:
        model = Alumno
        fields = [
            'persona',
            'institucion',
            'matricula_escolar',
        ]

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = [
            'persona',
            'institucion',
        ]

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Asignatura
        fields = [
            'nombre',
            'institucion',
            'docentes',
        ]

class PlanAsignaturaSerializer(serializers.ModelSerializer):
    asignatura = serializers.CharField(source='get_asignatura')

    class Meta:
        fields = [
            'asignatura',
            'inicio',
            'final',
        ]

class ActividadSerializer(serializers.ModelSerializer):
    plan = serializers.CharField(source='get_plan')
    class Meta:
        model = Actividad
        fields = [
            'nombre',
            'descripcion',
            'fecha_de_entrega',
            'puntos_maximos',
            'plan',
        ]

class EntregaSerializer(serializers.ModelSerializer):
    alumno = serializers.CharField(source='get_alumno')
    actividad = serializers.CharField(source='get_actividad')
    class Meta:
        fields = [
            'alumno',
            'actividad',
            'estado',
            'puntos',
        ]

class CursoSerializer(serializers.ModelSerializer):
    institucion = serializers.CharField(source='get_institucion')
    
    class Meta:
        fields = [
            'nombre',
            'institucion',
            'asignaturas',
            'alumnos',
        ]