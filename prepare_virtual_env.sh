#!/bin/bash

# define environment as PROD
export stage=prod

# make migrations
python manage.py makemigrations