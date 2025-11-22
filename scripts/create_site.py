import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so Django can import the settings module
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site

site, created = Site.objects.update_or_create(
    id=getattr(settings, 'SITE_ID', 1),
    defaults={'domain': '127.0.0.1', 'name': 'Localhost'},
)

print('CREATED' if created else 'UPDATED', site.id, site.domain, site.name)
