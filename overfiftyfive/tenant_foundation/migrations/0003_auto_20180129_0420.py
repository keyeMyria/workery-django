# Generated by Django 2.0 on 2018-01-29 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0002_auto_20180129_0229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='owner',
            new_name='created_by',
        ),
    ]
