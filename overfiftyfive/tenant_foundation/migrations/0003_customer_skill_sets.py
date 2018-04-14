# Generated by Django 2.0.4 on 2018-04-14 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0002_auto_20180413_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='skill_sets',
            field=models.ManyToManyField(blank=True, help_text='The skill sets this customer has.', related_name='tenant_foundation_customer_skill_sets_related', to='tenant_foundation.SkillSet'),
        ),
    ]
