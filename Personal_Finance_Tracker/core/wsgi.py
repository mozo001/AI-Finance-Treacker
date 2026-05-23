"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(str(BASE_DIR), 'db.sqlite3'),
        conn_max_age=600,
        ssl_require=True
    )
}
application = get_wsgi_application()
app = application
