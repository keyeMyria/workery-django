# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from tenant_foundation.models.abstract_thing import AbstractThing


class OpeningHoursSpecificationManager(models.Manager):
    def delete_all(self):
        items = OpeningHoursSpecification.objects.all()
        for item in items.all():
            item.delete()


class OpeningHoursSpecification(AbstractThing):
    """
    A structured value providing information about the opening hours of a place or a certain service inside a place.

    https://schema.org/OpeningHoursSpecification
    """
    class Meta:
        app_label = 'tenant_foundation'
        db_table = 'o55_opening_hours_specifications'
        verbose_name = _('Opening Hours Specification')
        verbose_name_plural = _('Opening Hours Specifications')
        default_permissions = ()
        permissions = (
            ("can_get_tenant_opening_hours_specifications", "Can get opening hours specifications (tenant)"),
            ("can_get_tenant_opening_hours_specification", "Can get opening hours specifications (tenant)"),
            ("can_post_tenant_opening_hours_specification", "Can create opening hours specifications (tenant)"),
            ("can_put_tenant_opening_hours_specification", "Can update opening hours specifications (tenant)"),
            ("can_delete_tenant_opening_hours_specification", "Can delete opening hours specifications (tenant)"),
        )

    objects = OpeningHoursSpecificationManager()
    closes = models.CharField(
        _("Closes"),
        max_length=15,
        help_text=_('The closing hour of the place or service on the given day(s) of the week.'),
        blank=True,
        null=True,
    )
    day_of_week = models.CharField(
        _("Day Of Week"),
        max_length=15,
        help_text=_('The day of the week for which these opening hours are valid.'),
        blank=True,
        null=True,
    )
    opens = models.CharField(
        _("Opens"),
        max_length=15,
        help_text=_('The opening hour of the place or service on the given day(s) of the week.'),
        blank=True,
        null=True,
    )
    valid_from = models.DateField(
        _("Valid From"),
        help_text=_('The date when the item becomes valid.'),
        blank=True,
        null=True
    )
    valid_through = models.DateField(
        _("Valid Through"),
        help_text=_('The end of the validity of offer, price specification, or opening hours data.'),
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.name)