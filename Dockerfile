FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
USER root

# Añade odbcinst.ini
COPY odbcinst.ini /etc/

# Instala dependencias del sistema
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends at supervisor curl gnupg unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev \
    postgresql python3-scipy python3-numpy python3-pandas && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools msodbcsql17 && \
    # Añadir mssql-tools al PATH de forma global
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> /etc/bash.bashrc && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> /etc/environment && \
    # Limpiar caché de apt para reducir tamaño de imagen
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala el paquete mssql-django
RUN pip install --no-cache-dir mssql-django

# Crea el directorio de trabajo y de configuraciones de Supervisor
RUN mkdir /code
RUN mkdir -p /etc/supervisor/conf.d

RUN mkdir -p /var/run/supervisor

# Copia el archivo requirements.txt al directorio de trabajo
COPY ./requirements.txt /code/

# Establece el directorio de trabajo
WORKDIR /code

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación a /code
COPY . /code/

# Copia los archivos de configuración de Supervisor
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY django_script.conf /etc/supervisor/conf.d/django_script.conf

COPY init.sh /code/init.sh
RUN chmod +x /code/init.sh

RUN ln -sf /usr/share/zoneinfo/America/Mexico_City /etc/localtime && \
    echo "America/Mexico_City" > /etc/timezone

# Expone el puerto para la aplicación Django
EXPOSE 8080

# Ejecuta supervisord con el archivo de configuración principal
CMD ["bash", "/code/init.sh"]

