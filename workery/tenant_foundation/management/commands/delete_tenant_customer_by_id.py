# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email,
    int_or_none
)
from shared_foundation import constants
from shared_foundation.models import (
    SharedUser,
    SharedFranchise,
    SharedUser
)
from tenant_foundation.models import (
    Associate,
    # Comment,
    Customer,
    Organization,
    WorkOrder,
    # WorkOrderComment,
    Staff,
    Tag
)
from tenant_foundation.utils import *


class Command(BaseCommand):
    help = _('Command will create an executive account in our application.')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py delete_tenant_customer_by_id "london" 666
        """
        parser.add_argument('schema_name', nargs='+', type=str)
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):
        # Get the user inputs.
        schema_name = options['schema_name'][0]
        id = options['id'][0]

        try:
            franchise = SharedFranchise.objects.get(schema_name=schema_name)
        except SharedFranchise.DoesNotExist:
            raise CommandError(_('Franchise does not exist!'))

        # Connection will set it back to our tenant.
        connection.set_schema(schema_name, True) # Switch to Tenant.

        # Defensive Code: Prevent continuing if the email already exists.
        user = None
        if Customer.objects.filter(id=id).exists():
            # Create the user.
            customer = Customer.objects.get(id=id)
            user = customer.owner
            customer.delete()
            self.stdout.write(self.style.SUCCESS(_('Deleted "Customer" object.')))

            if user:
                user.delete()
                self.stdout.write(self.style.SUCCESS(_('Deleted "SharedUser" object.')))

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully deleted a tenant customer.'))
        )
