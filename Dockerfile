# pull official base image
FROM tiangolo/uvicorn-gunicorn:python3.9

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install netcat gcc postgresql -y \
    && apt-get clean -y

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY ./app ./
ENV LOG_LEVEL info
ENV PYTHONPATH=.