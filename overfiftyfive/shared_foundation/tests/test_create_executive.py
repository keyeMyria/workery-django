from django.core.management import call_command
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from django.urls import reverse
from shared_foundation import constants
from shared_foundation.models.o55_user import O55User
from shared_foundation.utils import (
    get_random_string,
    get_unique_username_from_email
)


class TestCreateExecutiveManagementCommand(TenantTestCase):
    """
    Console:
    python manage.py test shared_foundation.tests.test_create_executive
    """
    # Fixtures to support our unit tests with sample data.
    fixtures = ['sites', 'groups']

    def setUp(self):
        super(TestCreateExecutiveManagementCommand, self).setUp()
        self.c = TenantClient(self.tenant)

    def tearDown(self):
        users = O55User.objects.all()
        for user in users.all():
            user.delete()
        del self.client

    def test_command_with_success(self):
        call_command('create_executive_account', "bart@overfiftyfive.com", "123P@$$w0rd", "Bart", "Mika", verbosity=0)

    def test_command_with_duplicate_email_error(self):
        O55User.objects.create(
            first_name="Bart",
            last_name="Mika",
            email="bart@overfiftyfive.com",
            username=get_unique_username_from_email("bart@overfiftyfive.com"),
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        try:
            call_command('create_executive_account', "bart@overfiftyfive.com", get_random_string(), "Bart", "Mika", verbosity=0)
        except Exception as e:
            self.assertIsNotNone(e)
            self.assertIn("Email already exists", str(e))

    def test_command_with_bad_password_error(self):
        try:
            call_command('create_executive_account', "bart@overfiftyfive.com", "123password", "Bart", "Mika", verbosity=0)
        except Exception as e:
            self.assertIsNotNone(e)
            self.assertIn("Password", str(e))