from django.db import models

from vo.util.info import SYSTEM_NAMES, short_system_name, sector_py2vochar


SID_CHOICES = [(i, SYSTEM_NAMES[i]) for i in xrange(1, len(SYSTEM_NAMES))]
X_CHOICES = [(i, chr(i + ord('A'))) for i in xrange(0, 16)]
Y_CHOICES = [(i, 16 - i) for i in xrange(0, 16)]
Y_CHOICES.reverse()


class AbstractSector(models.Model):
    x = models.PositiveSmallIntegerField(choices=X_CHOICES)
    y = models.PositiveSmallIntegerField(choices=Y_CHOICES)
    sid = models.PositiveSmallIntegerField(choices=SID_CHOICES)

    class Meta:
        abstract = True
        unique_together = ('x', 'y', 'sid')
        ordering = ('sid', 'x', 'y')

    def __repr__(self):
        return self.location_str()

    def __unicode__(self):
        return self.location_str()

    def location_str(self):
        x, y = sector_py2vochar(self.x, self.y)
        return '%s %s-%d' % (self.system(), x, y)

    def system(self):
        """Returns the system name.
        """
        return SYSTEM_NAMES[self.sid]

    def short_system(self):
        """Returns the short string name of the system.
        """
        return short_system_name(self.system())
