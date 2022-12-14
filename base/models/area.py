from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class RuralArea(models.Model):
    owner = models.ForeignKey(
        'base.Owner', on_delete=models.SET_NULL, null=True, blank=False)

    code = models.CharField(verbose_name=_("Name"), max_length=255,
                            null=True, blank=False)

    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)

    geometry = models.GeometryField(verbose_name=_("Geometry"),
                                    null=True, blank=True)

    area = models.FloatField(verbose_name=_("Area"),
                             blank=True, null=True)

    centroid = models.PointField(verbose_name=_("Centroid"),
                                 blank=True, null=True)

    creation_date = models.DateTimeField(verbose_name=_("Creation date"),
                                         auto_now_add=True, editable=False)

    last_modification_date = models.DateTimeField(
        verbose_name=_("Last modification date"), auto_now=True)

    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)

    def __str__(self):
        return ' | '.join([self.owner.name, self.name])

    class Meta:
        ordering = ['id']
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')
