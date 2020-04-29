from django.contrib import admin

# Register your models here.
from .models import Clint, SmartMeters, Bill

admin.site.register(Clint)
admin.site.register(SmartMeters)
admin.site.register(Bill)
