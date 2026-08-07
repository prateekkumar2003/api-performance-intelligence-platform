import os

from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

app = Celery("config")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()

"""
This file connects your Django project with Celery.

Without this file:

Celery would not know your Django settings
tasks would not auto-discover
worker could not run properly

This is basically:

Celery bootstrap/configuration file

Usually placed at:

config/celery.py

Your code:

import os
from celery import Celery

Imports:

Python OS module
Celery class
1. Set Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

This tells Celery:

"Use Django settings from config/settings.py"

Exactly like Django does in:

manage.py
wsgi.py
asgi.py

Without this:
Celery cannot access:

DATABASES
INSTALLED_APPS
CELERY settings
Redis config

Equivalent conceptually:

Load Django project first
Then start Celery
2. Create Celery application
app = Celery("config")

Creates Celery app instance.

"config" is app name.

Think:

Main Celery controller object

This app manages:

tasks
queues
workers
schedules
broker connection
3. Load settings from Django settings.py
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

Tells Celery:

"Read configuration from Django settings"

and only load variables starting with:

CELERY_

Example in settings.py:

CELERY_BROKER_URL = "redis://redis:6379/0"

Celery automatically loads it.

Why namespace?

Without namespace:
Celery would scan ALL Django settings.

With namespace:

Only settings starting with CELERY_

Cleaner and safer.

4. Auto discover tasks
app.autodiscover_tasks()

This is VERY important.

It automatically searches all Django apps for:

tasks.py

Example:

users/tasks.py
metrics/tasks.py
alerts/tasks.py

Celery automatically registers all:

@shared_task

functions.

Without this:
you would need manual imports everywhere.
"""