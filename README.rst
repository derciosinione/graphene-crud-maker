# Graphene CRUD Maker

This is a project to auto generate a graphql crud using graphene django

## Requirements

- Python >= 3.6
- Django >= 2.2
- Graphene Django >= 2.0


## Quick start
-----------

## Installation

```bash
pip install graphene-crud-maker
```

## Create a Django project

```bash
django-admin startproject core .
```

## Add "graphene_crud_maker" to your INSTALLED_APPS setting like this:


```python
    INSTALLED_APPS = [
        ...
        'myapp',
        'graphene_crud_maker',
        'graphene_django',
    ]
```

*Note: "myapp" is the name of the app*

## Add GRAPHENE to your settings.py

define the schema location for Graphene in the settings.py file of your Django project:

link: https://docs.graphene-python.org/projects/django/en/latest/

```python
    GRAPHENE = {
        "ATOMIC_MUTATIONS": True,
        'SCHEMA': 'core.schema.schema.schema',
        "SCHEMA_INDENT": 4,
        "MIDDLEWARE": [
            "graphene_django.debug.DjangoDebugMiddleware",
            'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ]
    }
```

*Note name "core" is the name of the project*

## Add URLS to your urls.py

```python
    from django.conf.urls import url
    from django.views.decorators.csrf import csrf_exempt
    from graphql_jwt.decorators import jwt_cookie
    from graphene_django.views import GraphQLView

    urlpatterns = [
        # ...
        url(r"graphql", csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True)))),
    ]
```

## Create the app

```bash
python3 manage.py startapp myapp
```

*Note: create models*


## Usage

### Python

```bash
python3 manage.py maker --help
```

### Output

```bash
Create Graphene CRUD

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  App name to create the CRUD graphQL
  -e [EXCLUDE ...], --exclude [EXCLUDE ...]
                        Fields to exclude in the CRUD (id, createdAt, updatedAt)

                        ...
```

## Command to create GraphQL

```bash
python3 manage.py maker -n myapp
```

## Run the server

```bash
python3 manage.py runserver
```

## GraphiQL

```bash
http://localhost:8000/graphql
```
