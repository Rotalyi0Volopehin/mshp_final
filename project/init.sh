#!/bin/bash


# requirements
pip install --upgrade pip
pip install -r ../src/web/requirements.txt
pip install -r ../src/desktop/requirements.txt

# django init
cd ../src/web
python manage.py migrate
python manage.py createsuperuser --username "vasya" --email "1@abc.net"
