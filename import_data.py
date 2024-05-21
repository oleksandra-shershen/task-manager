import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_service.settings')
application = get_wsgi_application()

with open('dump_json/data.json', 'r', encoding='utf-8') as f:
    call_command('loaddata', f.name)
