# Generated by Django 2.0.4 on 2018-04-27 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0008_auto_20180427_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='last_modified',
            new_name='last_modified_at',
        ),
    ]
