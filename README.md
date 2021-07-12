# Cadastro de Estudantes :school: :mortar_board:

Esse aplicativo serve para cadastrar os estudantes nos cursos que desejam cursar.

## Serviços

Método | URL | Ação
-------|-----|-------
POST | /api/curso | Cria uma nova cerveja
GET | /api/curso | Lista todos os cursos
GET | /api/curso?nome=`:nome` | Lista cursos com parte do nome como `:nome`
GET | /api/curso?codigo=`:codigo` | Busca o curso com o código `:codigo`
GET | /api/curso?matricula=`:matricula` | Lista os cursos do estudante com matrícula `:matricula`
PUT | /api/curso | Edita os dados de um curso
DELETE | /api/curso | Deleta um curso
POST | /api/estudante | Cria um novo estudante
GET | /api/estudante | Lista os estudantes
GET | /api/estudante?nome=`:nome` | Busca estudantes pelo `:nome`
GET | /api/estudante?matricula=`:matricula` | Busca um estudante pelo número de `:matricula`
GET | /api/estudante?codigo=`:codigo` | Lista estudantes matriculados no curso com código `:codigo`
PUT | /api/estudante | Edita os dados de um estudante
DELETE | /api/estudante | Deleta um estudante
POST | /api/cursar | Matricula um estudante em um curso
GET | /api/cursar | Lista todas as matrículas
GET | /api/cursar?matricula=`:matricula` | Busca as matrículas de um estudante pelo número de `:matricula`
GET | /api/cursar?codigo=`:codigo` | Lista os estudantes matriculados no curso com código `:codigo`
PUT | /api/cursar | Edita os dados de uma matrícula
DELETE | /api/cursar | Deleta uma matrícula

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