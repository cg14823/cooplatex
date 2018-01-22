# CoopLaTeX

Status: <strong>development</strong>

CoopLateX is a web application for creating, editing and compiling LaTeX projects


## Setup

This project is based on Django@1.11, Python 3.6 and PostgresSQL for the backend. This project was deployed using AWS.
For compiling the project you must also run the compiler server.

## Preview
__Home Page__
![alt-text](https://user-images.githubusercontent.com/10977025/35212378-cfe521a8-ff51-11e7-9b44-f84fa7fbf543.PNG)

__Editor Page__
![alt-text](https://user-images.githubusercontent.com/10977025/35212376-cfc96120-ff51-11e7-90f5-ae0da2aba3e8.PNG)

## Running

To run the service use

```
python manage.py runserver
```
 This will start the service on `localhost:8000`. You must set-up the following
 environmental variables before hand:
 
`ALLOWED_HOST`: For web deployment

`AWS_ACCESS_KEY_ID`: AWS access key ID

`AWS_SECRET_ACCESS_KEY`: AWS access key

`BUCKET_NAME`: S3 Bucket

`COMPILER_HOST`: URL of the compiler server

`COMPILER_SECRET_KEY`: Token to be added to all requests to the compiler

`EMAIL_PASS`: For email account verification

`RDS_DB_NAME`:AWS DB name

`RDS_HOSTNAME`: AWS RDS Host

`RDS_PASSWORD`: AWS RDS password

`RDS_PORT`: AWS RDS PORT

`RDS_USERNAME`: AWS RDS username

`SECRET_KEY`: Django secret key
