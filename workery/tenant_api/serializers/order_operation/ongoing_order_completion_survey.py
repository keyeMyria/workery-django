# -*- coding: utf-8 -*-
import logging
import phonenumbers
from datetime import datetime, timedelta
from dateutil import tz
from starterkit.drf.validation import (
    MatchingDuelFieldsValidator,
    EnhancedPasswordStrengthFieldValidator
)
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email
)
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from shared_api.custom_fields import PhoneNumberField
from shared_foundation.constants import CUSTOMER_GROUP_ID
from shared_foundation.models import SharedUser
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Comment,
    Associate,
    WorkOrder,
    ONGOING_WORK_ORDER_STATE,
    Organization,
    OngoingWorkOrder,
    OngoingWorkOrderComment,
    TaskItem
)


logger = logging.getLogger(__name__)


def get_todays_date_plus_days(days=0):
    """Returns the current date plus paramter number of days."""
    return timezone.now() + timedelta(days=days)


def cannot_be_zero_or_negative(value):
    if value <= 0:
        raise serializers.ValidationError('Please pick a reason from the dropdown.')
    return value


class OngoingWorkOrderCompletionSurveyOperationSerializer(serializers.Serializer):
    ongoing_job = serializers.PrimaryKeyRelatedField(many=False, queryset=OngoingWorkOrder.objects.all(), required=True)
    reason = serializers.CharField(required=True, allow_blank=False)

    # Meta Information.
    class Meta:
        fields = (
            'ongoing_job',
            'reason',
        )

    # def validate(self, data):
    #     """
    #     Override the validator to provide additional custom validation based
    #     on our custom logic.
    #
    #     1. If 'reason' == 1 then make sure 'reason_other' was inputted.
    #     """
    #     # CASE 1 - Other reason
    #     if data['reason'] == 1:
    #         reason_other = data['reason_other']
    #         if reason_other == "":
    #             raise serializers.ValidationError(_("Please provide a reason as to why you chose the \"Other\" option."))
    #     return data  # Return our data.

    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """
        #-------------------------#
        # Get validated POST data #
        #-------------------------#
        ongoing_job = validated_data.get('ongoing_job', None)
        reason = validated_data.get('reason', None)

        #------------------------------------------#
        # Create any additional optional comments. #
        #------------------------------------------#
        comment_obj = Comment.objects.create(
            created_by=self.context['user'],
            last_modified_by=self.context['user'],
            text=reason,
            created_from = self.context['from'],
            created_from_is_public = self.context['from_is_public']
        )
        OngoingWorkOrderComment.objects.create(
            about=ongoing_job,
            comment=comment_obj,
        )

        # For debugging purposes only.
        logger.info("Job comment created.")

        #-------------------------#
        # Update the ongoing ongoing_job. #
        #-------------------------#
        ongoing_job.state = ONGOING_WORK_ORDER_STATE.RUNNING
        ongoing_job.latest_pending_task = None
        ongoing_job.save()

        # For debugging purposes only.
        logger.info("Updated ongoing ongoing job.")

        #---------------------------------#
        # Close all the TaskItem objects. #
        #---------------------------------#
        for task_item in TaskItem.objects.filter(ongoing_job=ongoing_job, is_closed=False):
            task_item.last_modified_by = self.context['user']
            task_item.last_modified_from = self.context['from']
            task_item.last_modified_from_is_public = self.context['from_is_public']
            task_item.is_closed = True
            task_item.closing_reason = 1  # (Other - choice.)
            task_item.closing_reason_other = 'Closed because master ongoing job was closed.'
            task_item.save()

        # Return our processed values.
        return validated_data
