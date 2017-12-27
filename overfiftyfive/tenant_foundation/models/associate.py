# -*- coding: utf-8 -*-
import csv
import pytz
from datetime import date, datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from starterkit.utils import (
    get_random_string,
    generate_hash,
    int_or_none,
    float_or_none
)
from shared_foundation.constants import *
from tenant_foundation.models import (
    AbstractBigPk,
    AbstractContactPoint,
    AbstractGeoCoordinate,
    AbstractPostalAddress
)
from tenant_foundation.utils import *


class AssociateManager(models.Manager):
    def delete_all(self):
        items = Associate.objects.all()
        for item in items.all():
            item.delete()


class Associate(AbstractBigPk, AbstractContactPoint, AbstractPostalAddress, AbstractGeoCoordinate):
    class Meta:
        app_label = 'tenant_foundation'
        db_table = 'o55_associates'
        verbose_name = _('Associate')
        verbose_name_plural = _('Associates')

    objects = AssociateManager()

    #
    #  CUSTOM FIELDS
    #

    given_name = models.CharField(
        _("Given Name"),
        max_length=63,
        help_text=_('The employees given name.'),
        blank=True,
        null=True,
    )
    middle_name = models.CharField(
        _("Middle Name"),
        max_length=63,
        help_text=_('The employees last name.'),
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=63,
        help_text=_('The employees last name.'),
        blank=True,
        null=True,
    )
    business = models.CharField(
        _("Business"),
        max_length=63,
        help_text=_('The employees business status.'),
        blank=True,
        null=True,
    )
    birthdate = models.DateTimeField(
        _('Birthdate'),
        help_text=_('The employees birthdate.'),
        blank=True,
        null=True
    )
    join_date = models.DateTimeField(
        _("Join Date"),
        help_text=_('The date the employee joined.'),
        null=True,
        blank=True,
    )
    # area_served = ldn_area
    hourly_salary_desired = models.PositiveSmallIntegerField(
        _("Hourly Salary Desired"),
        help_text=_('The hourly salary rate the employee'),
        null=True,
        blank=True,
    )
    limit_special = models.CharField(
        _("Limit Special"),
        max_length=255,
        help_text=_('Any special limitations / handicaps this employee has.'),
        blank=True,
        null=True,
    )
    dues_pd = models.DateTimeField(
        _("Deus PD"),
        help_text=_('-'),
        null=True,
        blank=True,
    )
    ins_due = models.DateTimeField(
        _("Ins Due"),
        help_text=_('-'),
        null=True,
        blank=True,
    )
    police_check = models.DateTimeField(
        _("Police Check"),
        help_text=_('The date the employee took a police check.'),
        null=True,
        blank=True,
    )
    comments = models.CharField(
        _("Comments"),
        max_length=1027,
        help_text=_('The comments associated with this employee.'),
        blank=True,
        null=True,
    )
    drivers_license_class = models.CharField(
        _("Divers License Class"),
        max_length=7,
        help_text=_('The employees license class for driving.'),
        blank=True,
        null=True,
    )
    has_car = models.BooleanField(
        _("Has Car"),
        help_text=_('Indicates whether employee has a car or not.'),
        default=False,
        blank=True
    )
    has_van = models.BooleanField(
        _("Has Van"),
        help_text=_('Indicates whether employee has a van or not.'),
        default=False,
        blank=True
    )
    has_truck = models.BooleanField(
        _("Has Truck"),
        help_text=_('Indicates whether employee has a truck or not.'),
        default=False,
        blank=True
    )
    is_full_time = models.BooleanField(
        _("Is Full Time"),
        help_text=_('Indicates whether employee is full time or not.'),
        default=False,
        blank=True
    )
    is_part_time = models.BooleanField(
        _("Is Part Time"),
        help_text=_('Indicates whether employee is part time or not.'),
        default=False,
        blank=True
    )
    is_contract_time = models.BooleanField(
        _("Is Contract Time"),
        help_text=_('Indicates whether employee is contracted or not.'),
        default=False,
        blank=True
    )
    is_small_job = models.BooleanField(
        _("Is Small Job"),
        help_text=_('Indicates whether employee is employed for small jobs or not.'),
        default=False,
        blank=True
    )
    how_hear = models.CharField(
        _("How hear"),
        max_length=2055,
        help_text=_('How employee heared about this business.'),
        blank=True,
        null=True,
    )

    #
    #  SYSTEM FIELDS
    #

    user = models.OneToOneField(
        User,
        help_text=_('The user whom owns this associate.'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        db_index=True,
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True,)
    last_modified = models.DateTimeField(auto_now=True, db_index=True,)

    #
    #  FUNCTIONS
    #

    def __str__(self):
        if self.middle_name:
            return str(self.given_name)+" "+str(self.middle_name)+" "+str(self.last_name)
        else:
            return str(self.given_name)+" "+str(self.last_name)
