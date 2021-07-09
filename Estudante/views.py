from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Curso
from .serializers import CursoSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cursos(request):
    if request.method == 'GET':
        c = Curso.objects.all()

        nome = request.query_params.get('nome', None)
        codigo = request.query_params.get('codigo', None)
        if nome is not None:
            c = c.filter(nome__contains=nome)
        if codigo is not None:
            c = c.filter(codigo=codigo)
        cursos_serializer = CursoSerializer(c, many=True)
        return JsonResponse(cursos_serializer.data, safe=False)

    elif request.method == 'POST':
        curso_data = JSONParser().parse(request)
        curso_serializer = CursoSerializer(data=curso_data)
        if curso_serializer.is_valid():
            curso_serializer.save()
            return JsonResponse(curso_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(curso_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        curso_data = JSONParser().parse(request)
        nome = curso_data.get('nome', None)
        codigo = curso_data.get('codigo', None)

        if nome is not None and codigo is not None:
            c = Curso.objects.filter(codigo=codigo)
            if c is not None:
                c = c[0]
                c.nome = nome
                c.save()
                return JsonResponse({'message': f'Curso {nome} atualizado com sucesso'},
                                    status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message': 'Curso não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        curso_data = JSONParser().parse(request)
        codigo = curso_data.get('codigo', None)
        if codigo is not None:
            Curso.objects.filter(codigo=codigo).delete()
            return JsonResponse({'message': 'Curso excluído com sucesso'},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Curso não encontrado'}, status=status.HTTP_404_NOT_FOUND)
