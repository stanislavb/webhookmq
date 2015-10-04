import os
from django.core.wsgi import get_wsgi_application

os.getenv("DJANGO_SETTINGS_MODULE", "webhookmq.settings")
application = get_wsgi_application()
