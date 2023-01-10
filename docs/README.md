# FastAPI


![](endpoints.png)

Aplicação WEB - API usando FastAPI

O projeto será modelado no contexto de um Blog, afim de utilizar CRUD nas routes e diferentes tipos de Relacionamentos do banco de dados.

> - Para construir o projeto isolei cada aplicação em seu próprio ecosistema e embiente virtual. 
> - Ambos possuem a mesma estrutura e finalidade, porém aplicadas em Frameworks diferentes.

> [Progresso das **Tarefas**](tasks.md)

> [Progresso dos **Testes**](tests.md)

---
## Resumo 
- [FastAPI](#fastapi)
  - [Resumo](#resumo)
  - [Funcionalidades](#funcionalidades)
    - [Usuários](#usuários)
    - [Postagens](#postagens)
  - [Requisitos](#requisitos)
  - [Ambiente](#ambiente)
  - [Iniciar o servidor](#iniciar-o-servidor)
  - [Testes](#testes)
  - [Estrutura](#estrutura)
---

## Funcionalidades

### Usuários

- [x] Registro de novos usuários
- [x] Autenticação de usuários
- [x] Atualizar dados
- [x] Deletar conta

### Postagens

- [x] Criação de novo post
- [x] Edição de post
- [x] Remoção de post
- [x] Listagem de posts geral (home)
- [ ] Listagem de posts seguidos (timeline)
- [ ] Likes em postagens
- [ ] Postagem pode ser resposta a outra postagem


## Requisitos

- Git
- Python 3.10
- virtualenv ou semelhante
- Um editor de códigos como VSCode, Sublime, Vim, Pycharm ...


## Ambiente


Crie o ambiente virtual desta aplicação

```console
virtualenv .venv
```

Ative o ambiente 

```console
# Linux Bash
source .venv/bin/activate
# Windows Power Shell
./.venv/bin/activate.ps1
```

Instale as dependências

```console
pip install -r requirements.txt
# Teste
pip install -r requirements-test.txt
```

## Iniciar o servidor

Inicie o localhost


```console
uvicorn app:app --reload --factory
```

Acesse o docs de endpoints do Fastapi em:

http://127.0.0.1:8000/docs#/ ou http://127.0.0.1:8000/redoc/


## Testes

```console
cd tests
pytest
```

## Estrutura

```console
.
├── app
│   ├── controllers
│   │   ├── auth.py
│   │   ├── decorators
│   │   │   ├── auth_controller.py
│   │   │   ├── post_controller.py
│   │   │   └── user_controller.py
│   │   ├── post.py
│   │   └── user.py
│   ├── __init__.py
│   ├── models
│   │   ├── post
│   │   │   ├── __init__.py
│   │   │   ├── post.py
│   │   │   ├── request.py
│   │   │   └── response.py
│   │   ├── token
│   │   │   ├── __init__.py
│   │   │   └── token_model.py
│   │   └── user
│   │       ├── __init__.py
│   │       ├── request.py
│   │       ├── response.py
│   │       └── user.py
│   ├── routes.py
│   └── utils
│       ├── login_required.py
│       └── token_jwt.py
├── docs
│   ├── endpoints.png
│   ├── README.md
│   ├── tasks.md
│   └── tests.md
├── LICENSE
├── Procfile
├── requirements-test.txt
├── requirements.txt
├── runtime.txt
├── setup.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── models
    │   ├── __init__.py
    │   ├── test_post.py
    │   └── test_user.py
    ├── pytest.ini
    ├── routes
    │   ├── __init__.py
    │   ├── test_auth.py
    │   ├── test_post.py
    │   └── test_user.py
    ├── unity
    │   ├── __init__.py
    │   └── test_token_jwt.py
    └── utils
        ├── post.py
        ├── token.py
        └── user.py

14 directories, 45 files
```