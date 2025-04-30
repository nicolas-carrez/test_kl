"""
WSGI config for klaire project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Définir le module de configuration des paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'klaire.settings')

# Créer l'application WSGI pour le projet
application: "WSGIHandler" = get_wsgi_application()
