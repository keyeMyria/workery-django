# Generated by Django 2.0.4 on 2018-04-26 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0002_remove_customer_skill_sets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='skill_sets',
        ),
    ]
