# Generated by Django 2.0.4 on 2018-04-27 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0007_ordercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='associate',
            name='comments',
            field=models.ManyToManyField(blank=True, help_text='The comments belonging to this associate made by other people.', related_name='tenant_foundation_associate_associate_comments_related', through='tenant_foundation.AssociateComment', to='tenant_foundation.Comment'),
        ),
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.ManyToManyField(blank=True, help_text='The comments belonging to this order made by other people.', related_name='tenant_foundation_order_order_comments_related', through='tenant_foundation.OrderComment', to='tenant_foundation.Comment'),
        ),
        migrations.AddField(
            model_name='staff',
            name='comments',
            field=models.ManyToManyField(blank=True, help_text='The comments belonging to this staff made by other people.', related_name='tenant_foundation_staff_staff_comments_related', through='tenant_foundation.StaffComment', to='tenant_foundation.Comment'),
        ),
    ]
