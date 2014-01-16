from django.contrib import admin

from vo.nav.models import IonStorm, Obstacle


class IonStormAdmin(admin.ModelAdmin):
    list_display_links = list_display = ('sid', 'x', 'y', 'reported')
    list_filter = ('reported', 'sid',)


class ObstacleAdmin(admin.ModelAdmin):
    list_display_links = list_display = ('sid', 'x', 'y')
    list_filter = ('sid',)


admin.site.register(IonStorm, IonStormAdmin)
admin.site.register(Obstacle, ObstacleAdmin)
