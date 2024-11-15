from django.contrib import admin
from .models import *



@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    list_filter = ('status', 'region')

admin.site.register(Region)
admin.site.register(Commune)
admin.site.register(PropertyPrice)
admin.site.register(Proposal)