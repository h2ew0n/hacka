from django.contrib import admin
from .models import Mission, DeliveryStepView

# Register your models here.
admin.site.register(Mission)
admin.site.register(DeliveryStepView)