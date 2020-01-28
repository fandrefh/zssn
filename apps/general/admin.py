from django.contrib import admin

from .models import Item, Inventory, Survivor

# Register your models here.


class SurvivorAdmin(admin.ModelAdmin):
    list_display = ['name', 'longitude', 'latitude', 'infected']
    list_filter = ['infected']


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['survivor', 'item', 'quantity']
    list_filter = ['survivor', 'item']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'points']
    list_filter = ['name', 'points']


admin.site.register(Survivor, SurvivorAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Item, ItemAdmin)
