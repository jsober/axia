from django.contrib import admin

from vo.econ.models import Faction, Station, Item, SaleItem


class FactionAdmin(admin.ModelAdmin):
    pass


class StationAdmin(admin.ModelAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('item_name', 'item_id', 'volume')


class SaleItemAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('item', 'station', 'price')
    list_filter = ('station',)


admin.site.register(Faction, FactionAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
