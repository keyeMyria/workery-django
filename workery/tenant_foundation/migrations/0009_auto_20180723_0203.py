# Generated by Django 2.0.5 on 2018-07-23 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0008_customer_how_hear_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='how_hear',
            field=models.PositiveSmallIntegerField(blank=True, default=1, help_text='How customer heared/learned about this Over 55 Inc.', verbose_name='Learned about us'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='how_hear_other',
            field=models.CharField(blank=True, default='Did not answer', help_text='How customer heared/learned about this Over 55 Inc.', max_length=2055, verbose_name='Learned about us (other)'),
        ),
    ]