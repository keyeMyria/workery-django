# Generated by Django 2.0.4 on 2018-05-06 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0010_auto_20180506_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='closing_reason',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='The reason for this job order closing.', null=True, verbose_name='Closing Reason'),
        ),
        migrations.AddField(
            model_name='order',
            name='closing_reason_other',
            field=models.CharField(blank=True, default='', help_text='A specific reason this job order was closed.', max_length=1024, null=True, verbose_name='Closing Reason other'),
        ),
    ]