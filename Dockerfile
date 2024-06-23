# pull official base image
FROM python:3.10

RUN apt-get update
RUN apt-get install -y binutils libproj-dev libgdal-dev netcat-traditional 

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install poetry
RUN echo $(ls -l /usr/lib/)

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root
RUN pip install --upgrade --no-cache-dir setuptools==57.5.0
RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')
ENV GDAL_LIBRARY_PATH /usr/lib/libgdal.so

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
