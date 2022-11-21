# FastAPI

Aplicação WEB - API usando FastAPI

> - Para construir o projeto isolei cada aplicação em seu próprio ecosistema e embiente virtual. 
> - Ambos possuem a mesma estrutura e finalidade, porém aplicadas em Frameworks diferentes.
    

## Requisitos

- Python 3.10
- Um editor de códigos como VSCode, Sublime, Vim, Pycharm, Micro...


## Ambiente

Acesse a pasta fastapi no terminal

```console
cd fastapi/
```

Crie o ambiente virtual desta aplicação

```console
virtualenv .venv
```

Ative o ambiente 

```console
# Linux Bash
source .venv/bin/activate
# Windows Power Shell
.\venv\Scripts\activate.ps1
```

Instale as dependências

```console
pip install -r requirements.txt
# Teste
pip install -r requirements-test.txt
```


## Funcionalidades

### Usuários

- Registro de novos usuários
- Autenticação de usuários

### Postagens

- Criação de novo post
- Edição de post
- Remoção de post
- Listagem de posts geral (home)
- Listagem de posts seguidos (timeline)
- Likes em postagens
- Postagem pode ser resposta a outra postagem

## Estrutura

```console
.
├── app
│   ├── controllers
│   │   └── user_controller.py
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── requests
│   │   ├── responses
│   │   └── user.py
│   └── routes.py
├── docs
│   └── README.md
├── requirements.txt
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── models
    │   └── __init__.py
    └── routes
        └── __init__.py
```


## O Projeto

O projeto será modelado no contexto de um Blog, afim de utilizar CRUD nas routes e diferentes tipos de Relacionamentos do banco de dados.

Inicie o localhost

```console
cd fastapi/
```

```console
uvicorn app:app --reload --factory
```

Acesse o docs de endpoints do Fastapi em:

http://127.0.0.1:8000/docs#/ ou http://127.0.0.1:8000/redoc/

