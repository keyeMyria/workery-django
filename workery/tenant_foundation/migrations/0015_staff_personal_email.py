# Generated by Django 2.0.7 on 2018-08-08 00:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0014_auto_20180729_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='personal_email',
            field=models.EmailField(blank=True, db_index=True, help_text='The personal e-mail address of the staff member.', max_length=254, null=True, validators=[django.core.validators.EmailValidator(message='Invalid email')], verbose_name='Personal E-mail'),
        ),
    ]
