import os
from django.core.management.utils import get_random_secret_key

os.environ.setdefault('SECRET_KEY', get_random_secret_key())

from .settings import *  # noqa: F403, F401, E402


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache'

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
