"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

import django
from django.core.management import call_command


django.setup()


try:
    print("Avtomatik migratsiya boshlandi...")
    call_command("migrate", interactive=False)
    print("Avtomatik migratsiya muvaffaqiyatli yakunlandi!")
except Exception as e:
    print(f"Migratsiyada xatolik yuz berdi: {e}")