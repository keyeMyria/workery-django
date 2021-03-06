# -*- coding: utf-8 -*-
import csv
import pytz
from datetime import date, datetime, timedelta
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from shared_foundation import constants
from shared_foundation.models.abstract_thing import AbstractSharedThing
from shared_foundation.models.abstract_contact_point import AbstractSharedContactPoint
from shared_foundation.models.abstract_postal_address import AbstractSharedPostalAddress
from shared_foundation.models.abstract_geo_coorindate import AbstractSharedGeoCoordinate
from shared_foundation.models.user import SharedUser


class SharedFranchiseManager(models.Manager):
    def delete_all(self):
        items = SharedFranchise.objects.all()
        for item in items.all():
            item.delete()


class SharedFranchise(TenantMixin, AbstractSharedThing, AbstractSharedContactPoint, AbstractSharedPostalAddress, AbstractSharedGeoCoordinate):
    """
    Model is the tenant in our system.
    """

    class Meta:
        app_label = 'shared_foundation'
        db_table = 'workery_franchises'
        verbose_name = _('Franchise')
        verbose_name_plural = _('Franchises')
        default_permissions = ()
        permissions = (
            ("can_get_franchises", "Can get franchises"),
            ("can_get_franchise", "Can get franchise"),
            ("can_post_franchise", "Can post franchise"),
            ("can_put_franchise", "Can put franchise"),
            ("can_delete_franchise", "Can delete franchise"),
        )

    objects = SharedFranchiseManager()
    currency = models.CharField(
        _("Currency"),
        max_length=3,
        help_text=_('The currency used by this franchise formatted in <a href="https://en.wikipedia.org/wiki/ISO_4217">ISO 4217</a> formatting.'),
        default="CAD",
        blank=True,
    )
    timezone_name = models.CharField(
        _("Timezone Name"),
        max_length=63,
        help_text=_('The timezone for this tenant.'),
        default="America/Toronto",
        blank=True,
    )
    is_archived = models.BooleanField(
        _("Is Archived"),
        help_text=_('Indicates whether this franchise was archived.'),
        default=False,
        blank=True,
        db_index=True
    )

    #
    #  Custom Fields
    #

    #
    #  FUNCTIONS
    #

    def __str__(self):
        return str(self.name)

    def reverse(self, reverse_id, reverse_args=[]):
        return settings.WORKERY_APP_HTTP_PROTOCOL + str(self.schema_name) + "." + settings.WORKERY_APP_HTTP_DOMAIN + reverse(reverse_id, args=reverse_args)

    def is_public(self):
        """
        Function returns boolean value as to whether this franchise is the
        public or a tenant.
        """
        return self.schema_name == "public" or self.schema_name == "test"

    def to_tenant_dt(self, aware_dt):  #TODO: UNIT TEST
        """
        Function will convert the inputted timezone aware datetime object
        into the timezone specific to this tenant.
        """
        try:
            return aware_dt.astimezone(pytz.timezone(self.timezone_name))
        except Exception as e:
            return aware_dt

    def get_todays_date_plus_days(self, days=0):
        """Returns the current date plus paramter number of days."""
        utc_today = timezone.now()
        utc_todays_date = utc_today + timedelta(days=days)
        return self.to_tenant_dt(utc_todays_date)


class SharedFranchiseDomain(DomainMixin):
    class Meta:
        app_label = 'shared_foundation'
        db_table = 'workery_franchise_domains'
        verbose_name = _('Domain')
        verbose_name_plural = _('Domains')

    pass
