# -*- coding: utf-8 -*-
import datetime
from dateutil import parser
from djmoney.money import Money
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Extract
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from shared_foundation.constants import *
from shared_foundation.mixins import ExtraRequestProcessingMixin
from shared_foundation.utils import *
from tenant_api.filters.customer import CustomerFilter
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Associate,
    AwayLog,
    Customer,
    WORK_ORDER_STATE,
    WorkOrder,
    TaskItem,
    SkillSet
)

"""
Code below was taken from:
https://docs.djangoproject.com/en/2.0/howto/outputting-csv/
"""

import csv
from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def report_13_streaming_csv_view(request):
    from_dt = request.GET.get('from_dt', None)
    to_dt = request.GET.get('to_dt', None)
    state = request.GET.get('state', 'all')
    skillset_ids = request.GET.get('skillset_ids', None)

    skillset_ids_arr = skillset_ids.split(",")
    for idx, val in enumerate(skillset_ids_arr):
        skillset_ids_arr[idx] = int(val)

    from_dt = parser.parse(from_dt)
    to_dt = parser.parse(to_dt)

    queryset = None
    if state == 'all':
        queryset = WorkOrder.objects.filter(
            Q(skill_sets__in=skillset_ids_arr) &
            Q(assignment_date__range=(from_dt,to_dt))
        ).order_by(
            '-assignment_date'
        ).prefetch_related(
            'customer',
            'associate',
            'skill_sets'
        )
    else:
        queryset = WorkOrder.objects.filter(
            Q(skill_sets__in=skillset_ids_arr) &
            Q(state=state) &
            Q(assignment_date__range=(from_dt,to_dt))
        ).order_by(
            '-assignment_date'
        ).prefetch_related(
            'customer',
            'associate',
            'skill_sets'
        )

    # Defensive Code: If nothing is found then return nothing.
    if queryset.count() == 0:
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename="leads_by_skill.csv"'
        return response

    # Convert our aware datetimes to the specific timezone of the tenant.
    today = timezone.now()
    today = request.tenant.to_tenant_dt(today)
    from_dt = request.tenant.to_tenant_dt(from_dt)
    from_dt = from_dt.date()
    to_dt = request.tenant.to_tenant_dt(to_dt)
    to_dt = to_dt.date()

    # Generate our new header.
    rows = (["Leads by Skill Report","","","","","","","","","",],)
    rows += (["Report Date:", pretty_dt_string(today),"","","","","","","","",],)
    rows += (["From Assignment Date:", pretty_dt_string(from_dt),"","","","","","","","",],)
    rows += (["To Assignment Date:", pretty_dt_string(to_dt),"","","","","","","","",],)
    rows += (["Job Status:", str(state),"","","","","","","","",],)
    # rows += (["Skill Set(s):", str(state),"","","","","","","","",],)
    rows += (["","","","","","","","","","",],)
    rows += (["","","","","","","","","","",],)


    # Address	City	Phone	E-Mail	Associate	Associate Phone	Associate Email

    # Generate the CSV header row.
    rows += ([
        "Job No.",
        "Assignment Date",
        "Job Completion Date",
        "Client No.",
        "Client Name",
        "Client Address",
        "Client Phone",
        "Client E-Mail",
        "Job Skill Set(s)",
        "Associate Name",
        "Associate Phone",
        "Associate E-Mail"
    ],)

    # Generate hte CSV data.
    for job in queryset.iterator():
        # Get the type of job from a "tuple" object.
        test = dict(JOB_TYPE_OF_CHOICES)
        job_type = test[job.type_of]

        # Attach all the skill sets that are associated with each job.
        skill_set_string = job.get_skill_sets_string()

        # Generate the row.
        rows += ([
            job.id,
            pretty_dt_string(job.assignment_date),
            pretty_dt_string(job.completion_date),
            job.customer.id,
            str(job.customer),
            job.customer.get_postal_address_without_postal_code(),
            str(job.customer.telephone),
            job.customer.email,
            skill_set_string,
            str(job.associate),
            str(job.associate.telephone),
            job.associate.email,
        ],)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="leads_by_skill.csv"'
    return response
