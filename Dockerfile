# pull official base image
FROM tiangolo/uvicorn-gunicorn:python3.9

# create the app user
RUN addgroup --system app && adduser --system --group app

WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install apt-utils -y

RUN apt-get -y install netcat gcc postgresql -y \
    && apt-get clean -y \

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
COPY ./app /app

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
# Switch to a non-root user, which is recommended by Heroku.
USER app