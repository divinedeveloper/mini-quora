# mini-quora
Multitenant Question and answer based application

Core Requirements:-

    - Ubuntu 14.04, Python 2.7.6, Django 1.8.9, Pytest 3.1.0, git 1.9.1, Mysql 5.5, pip and virtual env
    - Other requirement can be found in requirements.txt file 


#Mysql setup
	- create database mini_quora with both username and password as root

#Clone GitHub repository

    - git clone https://github.com/divinedeveloper/mini-quora.git


#Create virtual env for first time only

    - cd mini-quora/

    - virtualenv env


#Activate virtual env from second time

    - source env/bin/activate


#Install requirements using pip

    - pip install -r requirements.txt

#Apply migrations to database

	- python manage.py migrate

#Populate fake data

	- python manage.py loadtestdata --generate-fk follow_fk api.User:20 api.Question:20 api.Answer:20 api.Tenant:10

#Run Unit tests

	- cd core

	- pytest -v -m unittest --ds=core.settings

#Run Server

	- cd ..

	- python manage.py runserver

#Go to Url

	- http://127.0.0.1:8000/

#Postman Collection

	- https://www.getpostman.com/collections/0be5abc21dc07cfc438d

