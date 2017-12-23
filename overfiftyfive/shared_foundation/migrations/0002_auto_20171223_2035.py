# Generated by Django 2.0 on 2017-12-23 20:35

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('shared_foundation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='O55User',
            fields=[
            ],
            options={
                'verbose_name': 'O55 User',
                'verbose_name_plural': 'O55 Users',
                'ordering': ('-email',),
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='sharedfranchise',
            name='frontline_staff',
            field=models.ManyToManyField(blank=True, help_text='The office staff and or volunteers who belong to this "Franchise".', related_name='shared_foundation_sharedfranchise_frontline_staff_related', to='shared_foundation.O55User'),
        ),
        migrations.AddField(
            model_name='sharedfranchise',
            name='managers',
            field=models.ManyToManyField(blank=True, help_text='The managers who belong to this "Franchise" and are administrators or have executive decision making authority.', related_name='shared_foundation_sharedfranchise_managers_related', to='shared_foundation.O55User'),
        ),
    ]