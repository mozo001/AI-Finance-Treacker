import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Find the absolute paths to your project base directories
BASE_DIR = Path(__file__).resolve().parent.parent

# Force-insert your base paths into Python's module lookup table
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'core'))

load_dotenv(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Vercel entrypoint target matching your vercel.json
app = application
