import secrets
import os


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', secrets.token_hex(36))
DEBUG = os.environ.get('DJANGO_DEBUG', False)
ALLOWED_HOSTS = ['localhost', '127.0.0.1','web']
