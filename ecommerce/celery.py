import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")


app = Celery("ecommerce")  # name of the root package

""" Celery will look for a tasks.py file in each application directory to load asynchronous
tasks defined in it. """

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
