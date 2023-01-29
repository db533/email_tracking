#!/bin/bash

# make migrations
python manage.py makemigrations
python manage.py migrate
