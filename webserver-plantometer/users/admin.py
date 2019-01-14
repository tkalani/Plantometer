from __future__ import unicode_literals
from django.contrib import admin
from .models import Users, Plants


#  CLASSESS  ARE  REGISTERES  HERE
admin.site.register(Plants)
admin.site.register(Users)