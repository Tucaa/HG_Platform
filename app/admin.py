from django.contrib import admin

from .models import RiverBasin, Location, Graph, Data

# Register your models here.

#Change name of room, topic 
admin.site.register(RiverBasin)
admin.site.register(Location)
admin.site.register(Data)
admin.site.register(Graph)
