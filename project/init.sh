#!/bin/bash


# requirements
pip install --upgrade pip
pip install -r ../src/web/requirements.txt

# django init
cd ../src/web
python manage.py migrate
