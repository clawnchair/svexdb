"""
Overrides settings.py
"""

SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# you can also use environment variables to store secret values
# import os
# SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydatabase',                      # Or path to database file if using sqlite3.
        'USER': 'mydatabaseuser',                      # Not used with sqlite3.
        'PASSWORD': 'mypassword',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',
    }
}

# Cache
# https://docs.djangoproject.com/en/2.0/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

ADMIN_URL = 'admin/'  # must end with /

REDDIT = {  # LOCAL CREDENTIALS
    'user-agent': 'your user agent',
    'client_id': 'xxxxxxxxxxxxxx',
    'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',

    'client_id_alt': 'xxxxxxxxxxxxxx',
    'client_secret_alt': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'refresh_token_alt': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
}
