FROM postgres:14.2

COPY app/database/database.sql /docker-entrypoint-initdb.d/01.sql