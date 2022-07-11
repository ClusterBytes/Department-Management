# Department Management System

A simple and minimal system for managing common activities in a College Department.

## Clone the Project

    git clone git@github.com:ClusterBytes/Department-Management.git
    cd project_DMS

# Linux setup guide

## Set up virtual environment

- create a virtual enviroment [guide](https://docs.python.org/3/library/venv.html)
- activate virtual enviroment `source Venv/bin/activate`

## install requirements

- open the project root directory and run
- pip3 install requirementv2.txt

## set up local postgres database and configure

For installing postgres:-

    sudo apt install wget ca-certificates

    sudo apt update

    apt install postgresql postgresql-contrib

    sudo -u postgres psql

## Migrate and update database

    python manage.py migrate

    python manage.py makemigrations

## Create admin

    python manage.py createsuperuser

## inspect DB

    python manage.py inspectdb

## run server

    python manage.py runserver

run server in different port `python manage.py runserver 9000`
