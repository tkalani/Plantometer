from django.contrib import admin
from .models import weathersensors, plantsensors, reservoir

# DIFFERENT  CLASSESS  SA\\SRE REGISTERED  ON  DATABASE
admin.site.register(weathersensors)
admin.site.register(plantsensors)
admin.site.register(reservoir)