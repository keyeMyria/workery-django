# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from django.core.management import call_command
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from shared_foundation.constants import *
from shared_foundation.models import SharedFranchise
from shared_foundation.models import SharedUser
from shared_foundation.utils import get_jwt_token_and_orig_iat
from tenant_foundation.constants import *
from tenant_foundation.models import Associate, AwayLog, InsuranceRequirement, Staff, SkillSet, TaskItem, Tag, VehicleType, WorkOrderServiceFee


TEST_SCHEMA_NAME = "london"
TEST_USER_EMAIL = "bart@workery.ca"
TEST_USER_USERNAME = "bart@workery.ca"
TEST_USER_PASSWORD = "123P@$$w0rd"
TEST_USER_TEL_NUM = "123 123-1234"
TEST_USER_TEL_EX_NUM = ""
TEST_USER_CELL_NUM = "123 123-1234"


class TestTenantReportViews(TenantTestCase):
    """
    Console:
    python manage.py test tenant_report.tests.test_views.TestTenantReportViews
    """

    #------------------#
    # Setup Unit Tests #
    #------------------#

    def setup_tenant(tenant):
        """Tenant Schema"""
        tenant.schema_name = TEST_SCHEMA_NAME
        tenant.name='Over 55 (London) Inc.',
        tenant.alternate_name="Over55",
        tenant.description="Located at the Forks of the Thames in ...",
        tenant.address_country="CA",
        tenant.address_locality="London",
        tenant.address_region="Ontario",
        tenant.post_office_box_number="", # Post Offic #
        tenant.postal_code="N6H 1B4",
        tenant.street_address="78 Riverside Drive",
        tenant.street_address_extra="", # Extra line.

    @classmethod
    def setUpClass(cls):
        """
        Run at the beginning before all the unit tests run.
        """
        super().setUpClass()

    def setUp(self):
        """
        Run at the beginning of every unit test.
        """
        super(TestTenantReportViews, self).setUp()

        # Setup our app and account.
        call_command('init_app', verbosity=0)
        call_command('populate_tenant_content', TEST_SCHEMA_NAME, verbosity=0)
        call_command('populate_tenant_sample_db', TEST_SCHEMA_NAME, verbosity=0)

        # Create the account.
        call_command(
           'create_tenant_account',
           TEST_SCHEMA_NAME,
           MANAGEMENT_GROUP_ID,
           TEST_USER_EMAIL,
           TEST_USER_PASSWORD,
           "Bart",
           "Mika",
           TEST_USER_TEL_NUM,
           TEST_USER_TEL_EX_NUM,
           TEST_USER_CELL_NUM,
           "CA",
           "London",
           "Ontario",
           "", # Post Offic #
           "N6H 1B4",
           "78 Riverside Drive",
           "", # Extra line.
           verbosity=0
        )

        # Get user and credentials.
        user = SharedUser.objects.filter(email=TEST_USER_EMAIL).first()
        token, orig_iat = get_jwt_token_and_orig_iat(user)

        # Setup our clients.
        self.anon_c = TenantClient(self.tenant)
        self.auth_c = TenantClient(self.tenant, HTTP_AUTHORIZATION='JWT {0}'.format(token))
        self.auth_c.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        TaskItem.objects.update_or_create(
            id=1,
            defaults={
                'id': 1,
                'type_of': FOLLOW_UP_CUSTOMER_SURVEY_TASK_ITEM_TYPE_OF_ID,
                'title': _('Completion Survey'),
                'description': _('Please call up the client and perform the satisfaction survey.'),
                'due_date': timezone.now(),
                'is_closed': False,
                'job': None,
                'ongoing_job': None,
                # 'created_by': None,
                # created_from
                # created_from_is_public
                # last_modified_by
            }
        )

    def tearDown(self):
        """
        Run at the end of every unit test.
        """
        # Delete previous data.
        SharedUser.objects.delete_all()
        TaskItem.objects.delete_all()

        # Delete our clients.
        del self.anon_c
        del self.auth_c

        # Finish teardown.
        super(TestTenantReportViews, self).tearDown()

    def test_report_listing_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_reports_list_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))

    def test_report_1_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_01_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Service Fees Due Report', str(response.content))

    def test_report_2_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_02_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Associate Jobs Report', str(response.content))

    def test_report_3_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_03_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Service Fees by Skill Set Report', str(response.content))

    def test_report_4_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_04_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Cancelled Jobs Report', str(response.content))

    def test_report_5_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_05_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Associate Insurance Report', str(response.content))

    def test_report_6_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_06_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Associate Police Check Due Date Report', str(response.content))

    def test_report_7_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_07_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Associate Birthdays Report', str(response.content))

    def test_report_8_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_08_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Associate Skill Sets Report', str(response.content))

    def test_report_9_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_09_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Client Addresses Report', str(response.content))

    def test_report_10_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_10_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Jobs Report', str(response.content))

    def test_report_11_details_page(self):
        response = self.auth_c.get(self.tenant.reverse('workery_tenant_report_11_detail_master'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Reports', str(response.content))
        self.assertIn('Commercial Jobs Report', str(response.content))
