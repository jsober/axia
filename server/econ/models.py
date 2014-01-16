from django.db import models

from vo.util.models import AbstractSector


class Faction(models.Model):
    faction_id = models.PositiveSmallIntegerField(unique=True)
    faction_name = models.CharField(max_length=50, unique=True)

    def __repr__(self):
        return self.faction_name

    def __unicode__(self):
        return repr(self)


class Station(AbstractSector):
    station_id = models.PositiveSmallIntegerField(unique=True)
    station_name = models.CharField(max_length=50, unique=True)
    faction = models.ForeignKey(Faction)

    def __repr__(self):
        return '%s (%s @ %s)' % (self.station_name, self.faction, self.location_str())

    def __unicode__(self):
        return repr(self)


class Item(models.Model):
    item_id = models.PositiveSmallIntegerField(unique=True)
    item_name = models.CharField(max_length=50)
    volume = models.PositiveSmallIntegerField()

    def __repr__(self):
        return '%s (%dcu)' % (self.item_name, self.volume)

    def __unicode__(self):
        return repr(self)


class SaleItem(models.Model):
    item = models.ForeignKey(Item)
    station = models.ForeignKey(Station)
    price = models.SmallIntegerField()

    class Meta:
        unique_together = ('item', 'station')

    def __repr__(self):
        return '%s @ %s for %dc' % (self.item, self.station, self.price)

    def __unicode__(self):
        return repr(self)
