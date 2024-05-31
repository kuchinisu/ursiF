from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.curso.serializers import InstitucionSerializer
from .models import Institucion
from apps.utils.pagination import LargeSetPagination

class InstitucionesView(APIView):
    def get(self,request, fotmat=None):
        instituciones = Institucion.objects.all()

        if instituciones.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(instituciones, request)
            serializer = InstitucionSerializer(results, many=True)

            return paginator.get_paginated_response({'instituciones':serializer.data})
        else: 
            return Response({'error':'no hay instituciones registradas'}, status=status.HTTP_404_NOT_FOUND)
        
class InstitucionMatriculaView(APIView):
    def get(self, request, matricula, format=None):
        instituciones = Institucion.objects.filter(matricula=matricula)

        if instituciones.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(instituciones, request)
            serializer = InstitucionSerializer(results, many=True)

            return paginator.get_paginated_response({'institucion':serializer.data})
        else: 
            return Response({'error':'la institucion no existe o fue eliminada'}, status=status.HTTP_404_NOT_FOUND)

class InstitucionNombreView(APIView):
    def get(self, request, nombre, format=None):
        instituciones = Institucion.objects.filter(nombre=nombre)

        if instituciones.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(instituciones, request)
            serializer = InstitucionSerializer(results, many=True)

            return paginator.get_paginated_response({'instituciones':serializer.data})
        else: 
            return Response({'error':f'no hay resultados para "{nombre}"'}, status=status.HTTP_404_NOT_FOUND)

