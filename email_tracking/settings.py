"""
Django settings for email_tracking project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# https://djangostars.com/blog/configuring-django-settings-best-practices/
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

root = environ.Path(__file__) - 3  # get root of the project
SITE_ROOT = root()

env = environ.Env()
environ.Env.read_env(overwrite=True)  # reading .env file

#stage = env.str('stage', default='dev')
#print('stage:',stage)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('django_secret_key', default='django-insecure-&+l0bsg19f2+gxmpub74g)$7*yq0t0zn9o1^78b!a1q!^sx!jc')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('debug', default=False)
TEMPLATE_DEBUG = DEBUG
print('debug:',DEBUG)

ALLOWED_HOSTS = env('allowed_hosts', cast=[str])
print('ALLOWED_HOSTS:',ALLOWED_HOSTS)
# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'tracking_app.apps.TrackingAppConfig',
	#'django_hosts',
#	'ptrack',
	'rest_framework',
]

MIDDLEWARE = [
	#'django_hosts.middleware.HostsRequestMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	#'django_hosts.middleware.HostsResponseMiddleware',
	'tracking_app.middleware.SessionMiddleware',    # The middleware to save the session_key as a cookie
]

ROOT_URLCONF = 'email_tracking.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'email_tracking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
print('db_name:',env.str('db_name', default='email_tracking'))
DATABASES = {
	'default': {
		'ENGINE': 'djongo',
		'NAME': env.str('db_name', default='email_tracking'),
			'ENFORCE_SCHEMA': False,
			'CLIENT': {
				'host': env.str('mongodb_uri')
			}
		}
	}
#print('DATABASES:', DATABASES)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Riga'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


public_root = root.path('public/')
MEDIA_ROOT = public_root('media')
MEDIA_URL = env.str('MEDIA_URL', default='media/')
STATIC_ROOT = public_root(env.str('static_root', default='static'))
#STATIC_ROOT = env.str('static_root', default='static')
STATIC_URL = env.str('STATIC_URL', default='static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://ordinarycoders.com/blog/article/django-subdomains
#ROOT_HOSTCONF = 'email_tracking.hosts'
#DEFAULT_HOST = 'email'

#PTRACK_SECRET = env.str('PTRACK_SECRET', default='rrtNPNc6Y48SkrDPfsVbY2lyUR0zpZH3')

#PTRACK_APP_URL = env.str('allowed_hosts', default='localhost') # Example: PTRACK_APP_URL = "https://www.example.com"

# https://alwaysdjango.com/how-to-send-html-emails-in-django/
# https://stackoverflow.com/questions/28980480/django-sending-email-smtpserverdisconnected-connection-unexpectedly-closed
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'mail.dundlabumi.lv'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=env.str('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env.str('EMAIL_HOST_USER')
SERVER_EMAIL = env.str('EMAIL_HOST_USER')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
	'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ] # Added this based on ChatGPT suggestion
}

APPEND_SLASH=False