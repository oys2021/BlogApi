from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key')

DEBUG=False

ORS_ALLOW_ALL_ORIGINS   = True

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
]


CSRF_TRUSTED_ORIGINS = [
    'https://tb.up.railway.app/',
]