# entries/admin.py

from django.contrib import admin
from .models import Entry, Time, Workouts


admin.site.register(Entry)
admin.site.register(Time)
admin.site.register(Workouts)