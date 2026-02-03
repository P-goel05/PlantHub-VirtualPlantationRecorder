from django.contrib import admin
from .models import PlantTree , Nursery , NurseryPlant , NurseryTool
# Register your models here.
admin.site.register(PlantTree)
admin.site.register(Nursery)
admin.site.register(NurseryPlant)       
admin.site.register(NurseryTool)