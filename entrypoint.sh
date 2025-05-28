#!/bin/bash

# entrypoint.sh

# Crear directorio de logs si no existe
mkdir -p /code/logs
mkdir -p /var/log/supervisor

# Asegurar permisos correctos
chmod -R 777 /code/logs
chmod -R 777 /var/log/supervisor

# Ejecutar supervisord
exec supervisord -c /etc/supervisor/supervisord.conf

