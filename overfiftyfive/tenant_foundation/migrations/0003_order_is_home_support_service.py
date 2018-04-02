# Generated by Django 2.0.3 on 2018-04-02 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0002_remove_organization_parent_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_home_support_service',
            field=models.BooleanField(default=False, help_text='Track whether this order is a home support service request.', verbose_name='Is Home Support Service'),
        ),
    ]