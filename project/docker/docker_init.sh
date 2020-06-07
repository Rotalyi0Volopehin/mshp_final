#!/usr/bin/env bash

cd src/web/ || exit 1
python manage.py migrate
python manage.py collectstatic --noinput
