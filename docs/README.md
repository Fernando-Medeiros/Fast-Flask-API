<div align="center">
    <img align="center" src="https://img.shields.io/badge/Python-white?style=for-the-badge&logo=python&logoColor=yellow">
    <img align="center" src="https://img.shields.io/badge/Flask-white?style=for-the-badge&logo=flask&logoColor=black">    
    <img align="center" src="https://img.shields.io/badge/FastAPI-white?style=for-the-badge&logo=fastapi&logoColor=blue">
</div>

<br>

# Fast - Flask -> API

Projeto pessoal - Duas aplicações API com FastAPI e Flask - (CRUD+AUTH)

O objetivo deste projeto está em aplicar os meus conhecimentos atuais no embiente Web, desenvolvendo a criação de duas aplicações APIs.


## Objetivo 

#### Principal

- Criar a documentação
- Criar o diagrama de casos de uso (https://app.diagrams.net/)
- Modelar o banco de dados (MySql workbench)
- Desenvolver a mesma aplicação Web-API em ambos os Frameworks

#### Secundario

- Integrar com outros bancos de dados em nuvem
- Criar uma pequena aplicação front-end


## Estrutura

```console
.
├── docs
│   └── README.md
├── fastapi
│   ├── app
│   │   ├── controllers
│   │   │   ├── decorators
│   │   │   │   └── post_user.py
│   │   │   ├── exceptions
│   │   │   │   └── id_not_found.py
│   │   │   └── user_controller.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── post
│   │   │   │   └── __init__.py
│   │   │   └── user
│   │   │       ├── __init__.py
│   │   │       ├── user.py
│   │   │       ├── user_request.py
│   │   │       └── user_response.py
│   │   ├── routes.py
│   │   └── utils
│   │       └── jwt_security.py
│   ├── docs
│   │   ├── README.md
│   │   └── tasks.md
│   ├── requirements.txt
│   ├── setup.py
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       ├── models
│       │   ├── __init__.py
│       │   └── test_user.py
│       ├── routes
│       │   ├── __init__.py
│       │   └── test_user.py
│       ├── unity
│       │   ├── __init__.py
│       │   └── test_token_jwt.py
│       └── utils
│           ├── token.py
│           └── user.py
├── flask
│   ├── app
│   │   ├── controllers
│   │   │   └── user_controller.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── requests
│   │   │   ├── responses
│   │   │   └── user.py
│   │   └── routes.py
│   ├── docs
│   │   └── README.md
│   ├── requirements.txt
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       ├── models
│       │   └── __init__.py
│       └── routes
│           └── __init__.py
├── LICENSE
├── requirements-test.txt
└── runtime.txt
```