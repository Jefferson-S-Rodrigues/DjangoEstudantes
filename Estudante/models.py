from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class Estudante(models.Model):

    matricula = models.CharField("Matrícula", max_length=255, unique=True)
    nome = models.CharField("Nome", max_length=255)
    social = models.CharField("Nome social", max_length=255, null=True, blank=True)
    cpf = models.CharField(
        "CPF",
        primary_key=True,
        max_length=11,
        unique=True,
        validators=[MinLengthValidator(11, message="adicione os 11 dígitos sem ponto ou traço")]
    )
    nascimento = models.DateField('Data de nascimento')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'


class Curso(models.Model):

    codigo = models.CharField('Código do Curso', max_length=255, unique=True)
    nome = models.CharField('Nome do Curso', max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Cursando(models.Model):

    estudante = models.ForeignKey('Estudante', on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    ativo = models.BooleanField('Ativo', default=True)
    nota = models.IntegerField('Nota', default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])