import os
import sys
from pathlib import Path

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

provider = 'google'
# Try to get client/secret from settings SOCIALACCOUNT_PROVIDERS if present
client_id = None
secret = None
try:
    prov = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
    app_data = prov.get('APP', {})
    client_id = app_data.get('client_id')
    secret = app_data.get('secret')
except Exception:
    pass

# Fallback: allow values from environment variables if not present in settings
if not client_id:
    client_id = os.environ.get('SOCIALAPP_GOOGLE_CLIENT_ID')
if not secret:
    secret = os.environ.get('SOCIALAPP_GOOGLE_SECRET')

if not client_id or not secret:
    print('Could not find Google client_id/secret in settings.SOCIALACCOUNT_PROVIDERS or environment variables.')
    print('Options:')
    print(' - Add the credentials to settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"] and re-run')
    print(' - Set environment variables SOCIALAPP_GOOGLE_CLIENT_ID and SOCIALAPP_GOOGLE_SECRET and re-run')
    print(' - Or create the SocialApp manually in Django admin (Sites -> Social applications)')
    sys.exit(1)

site = Site.objects.get(id=getattr(settings, 'SITE_ID', 1))

app, created = SocialApp.objects.update_or_create(
    provider=provider,
    defaults={
        'name': 'Google',
        'client_id': client_id,
        'secret': secret,
    }
)
# Associate with site
if site not in app.sites.all():
    app.sites.add(site)

print(('CREATED' if created else 'UPDATED'), app.provider, app.client_id, 'sites:', list(app.sites.values_list('id', flat=True)))
