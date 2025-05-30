#!/bin/bash

# entrypoint.sh

# Crear directorios si no existen
mkdir -p /code/logs

chmod -R 755 /code/logs

# Ejecutar supervisord
exec supervisord -c /etc/supervisor/supervisord.conf
