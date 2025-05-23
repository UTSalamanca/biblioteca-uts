FROM python:3.12.1-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

ADD odbcinst.ini /etc/

RUN apt-get update -y && apt-get install -y \
    curl gnupg git unixodbc unixodbc-dev tdsodbc freetds-common \
    freetds-bin freetds-dev postgresql supervisor
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y && apt-get install -y unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev postgresql
RUN apt-get update && ACCEPT_EULA=Y apt-get -y install mssql-tools msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN apt-get update
RUN mkdir /code
WORKDIR /code
RUN mkdir -p /var/log/supervisor && \
    chmod -R 777 /var/log/supervisor
RUN mkdir -p /code/logs && \
    chmod -R 777 /code/logs
RUN mkdir -p /var/run && \
    chmod -R 777 /var/run
COPY . /code/
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install mssql-django numpy scipy pandas
# Crear un usuario no root
RUN useradd -ms /bin/bash userbiblioteca
# Cambiar el propietario de los archivos al nuevo usuario
RUN chown -R userbiblioteca:userbiblioteca /code /var/run
# Cambiar al nuevo usuario
USER userbiblioteca
EXPOSE 8080
