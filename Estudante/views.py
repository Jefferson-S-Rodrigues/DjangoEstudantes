from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Curso, Estudante, Cursando
from .serializers import CursoSerializer, EstudanteSerializer, CursandoSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def estudantes(request):
    if request.method == 'GET':
        _estudantes = Estudante.objects.all()

        _nome = request.query_params.get('nome', None)
        _matricula = request.query_params.get('matricula', None)
        _codigo = request.query_params.get('codigo', None)
        if _nome is not None:
            _estudantes = _estudantes.filter(nome__contains=_nome)
        if _matricula is not None:
            _estudantes = _estudantes.filter(matricula=_matricula)
        if _codigo is not None:
            _estudantes = _estudantes.filter(
                cpf__in=(Cursando.objects.filter(curso__codigo=_codigo).values('estudante')))
        estudantes_serializer = EstudanteSerializer(_estudantes, many=True)
        return JsonResponse(estudantes_serializer.data, safe=False)

    elif request.method == 'POST':
        estudante_data = JSONParser().parse(request)
        estudante_serializer = EstudanteSerializer(data=estudante_data)
        if estudante_serializer.is_valid():
            estudante_serializer.save()
            return JsonResponse(estudante_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(estudante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        estudante_data = JSONParser().parse(request)
        _nome = estudante_data.get('nome', None)
        _social = estudante_data.get('social', None)
        _nascimento = estudante_data.get('nascimento', None)
        _cpf = estudante_data.get('cpf', None)
        _matricula = estudante_data.get('matricula', None)

        if (
                _nome is not None or
                _social is not None or
                _nascimento is not None or
                _cpf is not None
        ) and _matricula is not None:
            _estudante = Estudante.objects.filter(matricula=_matricula).first()
            if _estudante is not None:
                if _nome is not None: _estudante.nome = _nome
                if _social is not None: _estudante.social = _social
                if _nascimento is not None: _estudante.nascimento = _nascimento
                if _cpf is not None: _estudante.cpf = _cpf
                _estudante.save()
                return JsonResponse({'message': f'Dados de {_estudante.nome} atualizados com sucesso'},
                                    status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message': 'Estudante não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        estudante_data = JSONParser().parse(request)
        _matricula = estudante_data.get('matricula', None)
        if _matricula is not None:
            Estudante.objects.filter(matricula=_matricula).delete()
            return JsonResponse({'message': 'Estudante excluído com sucesso'},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Estudante não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cursos(request):
    if request.method == 'GET':
        _curso = Curso.objects.all()

        _nome = request.query_params.get('nome', None)
        _codigo = request.query_params.get('codigo', None)
        _matricula = request.query_params.get('matricula', None)
        if _nome is not None:
            _curso = _curso.filter(nome__contains=_nome)
        if _codigo is not None:
            _curso = _curso.filter(codigo=_codigo)
        if _matricula is not None:
            _curso = _curso.filter(
                id__in=(Cursando.objects.filter(estudante__matricula=_matricula).values('curso'))
            )
        cursos_serializer = CursoSerializer(_curso, many=True)
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
        _nome = curso_data.get('nome', None)
        _codigo = curso_data.get('codigo', None)

        if _nome is not None and _codigo is not None:
            _curso = Curso.objects.filter(codigo=_codigo).first()
            if _curso is not None:
                _curso.nome = _nome
                _curso.save()
                return JsonResponse({'message': f'Curso {_nome} atualizado com sucesso'},
                                    status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message': 'Curso não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        curso_data = JSONParser().parse(request)
        _codigo = curso_data.get('codigo', None)
        if _codigo is not None:
            Curso.objects.filter(codigo=_codigo).delete()
            return JsonResponse({'message': 'Curso excluído com sucesso'},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Curso não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cursar(request):
    if request.method == 'GET':

        _cursando = Cursando.objects.all()

        _matricula = request.query_params.get('matricula', None)
        _codigo = request.query_params.get('codigo', None)
        if _codigo is not None:
            _cursando = _cursando.filter(curso=_codigo)
        if _matricula is not None:
            _cursando = _cursando.filter(estudante__matricula=_matricula)
        cursando_serializer = CursandoSerializer(_cursando, many=True)
        return JsonResponse(cursando_serializer.data, safe=False)

    elif request.method == 'POST':
        cursando_data = JSONParser().parse(request)
        _matricula = cursando_data.get('matricula', None)
        _codigo = cursando_data.get('codigo', None)
        _estudante = Estudante.objects.filter(matricula=_matricula).first()
        _curso = Curso.objects.filter(codigo=_codigo).first()
        if _estudante is not None and _curso is not None:
            _cursando = Cursando(estudante=_estudante, curso=_curso)
            _cursando.save()
            return JsonResponse(
                {'message': f'Matrícula de {_estudante.nome} no curso de {_curso.nome} realizada com sucesso'},
                status=status.HTTP_201_CREATED)
        return JsonResponse({'message': 'Não foi possível realizar a matrícula'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        cursando_data = JSONParser().parse(request)
        _matricula = cursando_data.get('matricula', None)
        _codigo = cursando_data.get('codigo', None)
        _nota = cursando_data.get('nota', None)
        _ativo = cursando_data.get('ativo', None)
        _estudante = Estudante.objects.filter(matricula=_matricula).first()
        _curso = Curso.objects.filter(codigo=_codigo).first()

        if _matricula is not None and _codigo is not None and (_ativo is not None or _nota is not None):
            _cursando = Cursando.objects.filter(estudante=_estudante).filter(curso=_curso).first()
            if _cursando is not None:
                if _nota is not None:
                    _cursando.nota = _nota
                if _ativo is not None:
                    _cursando.ativo = _ativo
                _cursando.save()
                return JsonResponse({'message': f'Dados atualizados com sucesso'},
                                    status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message': 'Não há matrícula para esse filtro'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        cursando_data = JSONParser().parse(request)
        _matricula = cursando_data.get('matricula', None)
        _codigo = cursando_data.get('codigo', None)
        _estudante = Estudante.objects.filter(matricula=_matricula).first()
        _curso = Curso.objects.filter(codigo=_codigo).first()
        if _codigo is not None:
            Cursando.objects.filter(curso=_curso).filter(estudante=_estudante).delete()
            return JsonResponse({'message': 'Matrícula excluída com sucesso'},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Matrícula não encontrada'}, status=status.HTTP_404_NOT_FOUND)
