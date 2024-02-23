FROM python:3.9.13-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ADD odbcinst.ini /etc/
RUN apt-get update -y && apt-get install -y curl gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y && apt-get install -y unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev postgresql python-scipy python-numpy python-pandas
RUN apt-get update && ACCEPT_EULA=Y apt-get -y install mssql-tools msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN apt-get update
RUN pip install mssql-django
RUN mkdir /code
COPY . /code/
COPY ./requirements.txt /code/
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080