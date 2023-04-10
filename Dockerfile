FROM python:3.10

RUN mkdir /app

RUN apt-get update
RUN apt-get install -y binutils libproj-dev libgdal-dev
RUN apt-get install -y postgresql-client

RUN pip install --upgrade pip
RUN pip install poetry
RUN echo $(ls -l /usr/lib/)

COPY . /app

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root
RUN pip install --upgrade --no-cache-dir setuptools==57.5.0
RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')
ENV GDAL_LIBRARY_PATH /usr/lib/libgdal.so

EXPOSE 8000

CMD ["sh", "docker-entrypoint.sh"]
