# Cadastro de Estudantes :school: :mortar_board:

Esse aplicativo serve para cadastrar os estudantes nos cursos que desejam cursar.

### Instalar os pacotes necessários para execução

```console
python3 -m pip install -r requirements.txt
```

### Configurar o Banco de Dados

```console
python3 manage.py makemigrations Curso Estudante
python3 manage.py migrate
```

## Executando o Ambiente

```console
python3 manage.py runserver
```

## Container

Para inserir o sistema em um container _Docker_, use o comando:

```console
docker-compose up -d
```