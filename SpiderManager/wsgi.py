"""
WSGI config for SpiderManager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from nmaptoolbackground.control import taskcontrol

import faulthandler
import pdb
from dozer import Dozer,Logview

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpiderManager.settings")

application = get_wsgi_application()
# application = Dozer(application)
# application = Logview(application)
faulthandler.enable()
taskcontrol.scheduleinit()
