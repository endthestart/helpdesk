import os
import sys

sys.path.append('/srv/www/helpdesktogo.com/')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/helpdesktogo.com/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] ='helpdesk.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
