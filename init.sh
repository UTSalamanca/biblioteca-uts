#!/bin/bash
mkdir -p /var/log/supervisor
touch /var/log/supervisor/django_script.log
touch /var/log/supervisor/django_script_err.log
chmod 644 /var/log/supervisor/django_script*.log

# Inicia supervisord en segundo plano para manejar la tarea programada
supervisord -c /etc/supervisor/supervisord.conf &

# Inicia supervisord
exec python /code/manage.py runserver 0.0.0.0:8080