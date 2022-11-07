from .prod import *

ALLOWED_HOSTS = ['testserver']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dev_db',
        'USER': 'postgres',
        'PASSWORD': 'test',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
