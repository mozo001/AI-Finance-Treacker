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

BASE_DIR = Path(__file__).resolve().parent.parent
<<<<<<< HEAD
sys.path.append(str(BASE_DIR))
=======
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
>>>>>>> 60e1e653dcc77deac03169f5a5537d6a03444de4

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
app = application
