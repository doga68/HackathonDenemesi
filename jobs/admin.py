from django.contrib import admin
from .models import Application, Job, Worker
admin.site.register([Job, Application, Worker])
