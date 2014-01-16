import datetime

from django.db import models
from django.utils.timezone import now

from vo.util.info import SYSTEM_NAMES, short_system_name
from vo.util.models import AbstractSector
from vo.util.nav import Sector, Point


class IonStormManager(models.Manager):
    def sectors(self):
        def sector(storm):
            point = Point(storm.x, storm.y)
            system = short_system_name(SYSTEM_NAMES[storm.sid])
            return Sector(system, point)

        stale = now() - IonStorm.MAX_DURATION
        storms = super(IonStormManager, self).get_query_set().filter(reported__gte=stale)
        return set(sector(s) for s in storms)


class IonStorm(AbstractSector):
    """Stores the location and reported time of an ion storm.
    """
    MAX_DURATION = datetime.timedelta(hours=4)

    reported = models.DateTimeField(auto_now=True)

    objects = IonStormManager()

    class Meta:
        ordering = ('-reported', 'sid', 'x', 'y')

    def __unicode__(self):
        sector = super(IonStorm, self).__unicode__()
        return '%s reported at %s' % (sector, self.reported)


class ObstacleManager(models.Manager):
    def sectors(self):
        def sector(s):
            point = Point(s.x, s.y)
            system = short_system_name(SYSTEM_NAMES[s.sid])
            return Sector(system, point)

        sectors = super(ObstacleManager, self).get_query_set().all()
        return set(sector(s) for s in sectors)


class Obstacle(AbstractSector):
    """Stores the location of a sector with asteroids,
    drones, or a station, which should be avoided as a
    waypoint on a route.
    """
    objects = ObstacleManager()
