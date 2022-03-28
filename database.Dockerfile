FROM postgres:14.2

copy database/database.sql /docker-entrypoint-initdb.d/01.sql