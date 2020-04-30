from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Clint)
admin.site.register(SmartMeters)
admin.site.register(Bill)
admin.site.register(Appliances)
admin.site.register(Seller)
admin.site.register(Factory)
admin.site.register(ApplianceCategory)


