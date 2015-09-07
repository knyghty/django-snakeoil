from __future__ import unicode_literals


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = [
    'snakeoil',
    'tests',
]

SECRET_KEY = 'fake-key'
