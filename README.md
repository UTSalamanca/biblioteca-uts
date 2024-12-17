# biblioteca_digital
Sistema de Gestión de Biblioteca de la Universidad Tecnológica de Salamanca

## Pre-requisitos

- Instalar [Docker.](https://www.docker.com/get-started)
- Instalar [Docker Compose.](https://docs.docker.com/compose/install/)

## Instalación

- Clonar repositorio `git clone https://github.com/Frank049600/biblioteca_digital.git`
- Entrar a la carpeta del proyecto `cd biblioteca-uts`
- Generar imagen docker**`docker-compose build`**
- Generar contenedores **`docker-compose up -d`**
- Crear migraciones `docker compose run biblioteca_uts python manage.py makemigrations`
- Ejecutar migraciones `docker compose run biblioteca_uts python manage.py migrate`
- Crear superusuario **`docker compose run biblioteca_uts python manage.py createsuperuser`**
- Configurar archivo **`.env`** si es necesario.
- Crear carpeta "media" a nivel del archivo requirements.txt

## Abrir proyecto

Abrir navegador y entrar a URL [127.0.0.1:8080](http://127.0.0.1:8080)
