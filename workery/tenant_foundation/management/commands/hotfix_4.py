# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email
)
from shared_foundation.constants import *
from shared_foundation.models import (
    SharedUser,
    SharedFranchise
)
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Associate,
    # Comment,
    Customer,
    InsuranceRequirement,
    Organization,
    WORK_ORDER_STATE,
    WorkOrder,
    # WorkOrderComment,
    WorkOrderServiceFee,
    ResourceCategory,
    ResourceItem,
    ResourceItemSortOrder,
    SkillSet,
    Staff,
    Tag,
    VehicleType,
    ONGOING_WORK_ORDER_STATE,
    OngoingWorkOrder
)
from tenant_foundation.utils import *


class Command(BaseCommand):
    help = _('Command will run `hotfix_4`. PLEASE RUN THIS ONLY ONCE!')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py hotfix_4 "london"
        """
        parser.add_argument('schema_name', nargs='+', type=str)

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.
        # Get the user inputs.
        schema_name = options['schema_name'][0]

        try:
            franchise = SharedFranchise.objects.get(schema_name=schema_name)
        except SharedFranchise.DoesNotExist:
            raise CommandError(_('Franchise does not exist!'))

        # Connection will set it back to our tenant.
        connection.set_schema(franchise.schema_name, True) # Switch to Tenant.

        customers = Customer.objects.all()
        for customer in customers.all():
            how_hear_text = customer.how_hear
            if how_hear_text:

                how_hear = 1
                how_hear_other = how_hear_text

                how_hear_text = how_hear_text.lower()
                if "friend" in how_hear_text:
                    how_hear = 2

                elif "google" in how_hear_text:
                    how_hear = 3

                elif "online" in how_hear_text:
                    how_hear = 3

                elif "internet" in how_hear_text:
                    how_hear = 3

                elif "inernet" in how_hear_text:
                    how_hear = 3

                elif "www" in how_hear_text:
                    how_hear = 3

                elif "website" in how_hear_text:
                    how_hear = 3

                elif "on line" in how_hear_text:
                    how_hear = 3

                elif "on-line" in how_hear_text:
                    how_hear = 3

                elif "computer" in how_hear_text:
                    how_hear = 3

                elif "associate" in how_hear_text:
                    how_hear = 5

                elif "facebook" in how_hear_text:
                    how_hear = 6

                elif "twitter" in how_hear_text:
                    how_hear = 7

                elif "instagram" in how_hear_text:
                    how_hear = 8

                elif "magazine" in how_hear_text:
                    how_hear = 9

                elif "event" in how_hear_text:
                    how_hear = 10

                customer.how_hear = int(how_hear)
                customer.how_hear_other = how_hear_other
                customer.save()

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully updated.'))
        )
