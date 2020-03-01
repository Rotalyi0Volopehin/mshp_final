#!/bin/bash

# virtualenv
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate

# requirements
pip install --upgrade pip
pip install -r ../src/web/requirements.txt

# django init
cd ../src/web
python manage.py migrate
