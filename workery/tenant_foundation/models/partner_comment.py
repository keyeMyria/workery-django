# -*- coding: utf-8 -*-
import csv
import pytz
from datetime import date, datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from starterkit.utils import (
    get_random_string,
    generate_hash,
    int_or_none,
    float_or_none
)
from shared_foundation.models import SharedUser
from shared_foundation.constants import *
from tenant_foundation.utils import *


class PartnerCommentManager(models.Manager):
    def delete_all(self):
        items = PartnerComment.objects.all()
        for item in items.all():
            item.delete()


@transaction.atomic
def increment_partner_comment_id_number():
    """Function will generate a unique big-int."""
    last_resource_item = PartnerComment.objects.all().order_by('id').last();
    if last_resource_item:
        return last_resource_item.id + 1
    return 1


class PartnerComment(models.Model):
    class Meta:
        app_label = 'tenant_foundation'
        db_table = 'workery_partner_comments'
        verbose_name = _('Partner Comment')
        verbose_name_plural = _('Partner Comments')
        ordering = ['-created_at']
        default_permissions = ()
        permissions = (
            ("can_get_partner_comments", "Can get partner comments"),
            ("can_get_partner_comment", "Can get partner comment"),
            ("can_post_partner_comment", "Can create partner comment"),
            ("can_put_partner_comment", "Can update partner comment"),
            ("can_delete_partner_comment", "Can delete partner comment"),
        )

    objects = PartnerCommentManager()
    id = models.BigAutoField(
       primary_key=True,
       default=increment_partner_comment_id_number,
       editable=False,
       db_index=True
    )

    #
    #  FIELDS
    #

    comment = models.ForeignKey(
        "Comment",
        help_text=_('The comment this item belongs to.'),
        related_name="%(app_label)s_%(class)s_comment_categories",
        on_delete=models.CASCADE,
    )
    about = models.ForeignKey(
        "Partner",
        help_text=_('The partner whom this comment is about.'),
        related_name="%(app_label)s_%(class)s_about_related",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    #
    #  FUNCTIONS
    #

    def __str__(self):
        return str(self.about)+" "+str(self.created_at)
