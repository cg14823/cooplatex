# CoopLaTeX

Status: <strong>development</strong>

CoopLateX is a web application for collaboratively creating, editing and sharing
LaTeX projects.


## Setup

This project is based on Django@1.11, Python 3.6 and PostgresSQL for the backend
Hopefully a Docker setup will be created soon to ease installation. For know 
install requirement usign `pip`.

## Running

To run the service use

```
python manage.py runserver
```
 This will start the service on `localhost:8000`. You must set-up the following
 environmental variables before hand:

`POSTGRES_HOST`: address of postgres server

`POSTGRES_USER`: user for the database

`POSTGRES_PASSWORD`: Password for the database
