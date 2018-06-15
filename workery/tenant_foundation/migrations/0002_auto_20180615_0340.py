# Generated by Django 2.0.5 on 2018-06-15 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associate',
            name='drivers_license_class',
            field=models.CharField(blank=True, help_text='The associates license class for driving.', max_length=15, null=True, verbose_name='Divers License Class'),
        ),
    ]