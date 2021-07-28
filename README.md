# car_api
Simple REST API which enables to post and get data about car makes and models.
Endpoints :
- /cars
- - POST cars, expected body 
    {"make": "make name", "model": "model name"}
    Existance of a car is checked here 
    https://vpic.nhtsa.dot.gov/api/
- - GET - returns list of all saved car objects
- /popular
- - GET - return list of top cars based on number of rates
- /rate
- - POST a rate for specific car, expected body
    {"make": "make name", "model": "model name", "rate": "4"}
    rates should be in range 1 - 5

## Frameworks
This project is built on most popular frameworks and third party packages used in web development :
- Django 3.1.6 
- Django REST framework 3.12.2
- Request 2.25.1 - this third party package is used to communicate with external API

Other libraries are mostly dependecies for Django and Django REST framework.

# Setup
Firstly You have to download the repo

```sh
$ git clone https://github.com/marekndt04/car_api.git
$ cd /path/to/car_api
```

Create new virtualenv and activate it

```sh
$ python3 -m venv /path/to/car_api/venv
$ source venv/bin/activate
```

Then You should install all dependencies
```sh
$ pip install -r requirements.txt
```

Project uses postgresql database, depending on your OS download postgres
https://www.postgresql.org/download/

If You are user of Linux or MacOS You can run 
```sh
$ psql postgres
```
and then in postgres shell You have to create a database and set a role
```sh
run command to create new ROLE
  =# CREATE ROLE django_app;
run command to create database
  =# CREATE DATABASE car_api;
run command to grant user abillity to log to postgres
  =# ALTER ROLE django_app WITH LOGIN;
run command to grant user all privileges to db;
  =# GRANT ALL PRIVILEGES ON DATABASE car_api TO django_app;
and quit
  =# \q
```

Now You can run command to start server.
```sh
$ python manage.py runserver 
```

Navigate to http://127.0.0.1:8000

# Tests
Tests use standard unittest.TestCase and django.test.TestCase.
To run them use command 
```sh
$ python manage.py test
```
