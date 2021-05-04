#!/bin/sh


set -e

# python manage.py collectstatic --noinput
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

uwsgi --socket :8000 --master --enable-threads --module atlantis.wsgi
# gunicorn dawir.wsgi -b 0.0.0.0:8000
