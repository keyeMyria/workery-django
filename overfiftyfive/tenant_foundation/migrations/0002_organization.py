# Generated by Django 2.0 on 2017-12-28 00:39

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant_foundation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('alternate_name', models.CharField(blank=True, help_text='An alias for the item.', max_length=255, null=True, verbose_name='Alternate Name')),
                ('description', models.TextField(blank=True, default='', help_text='A short description of the item.', null=True, verbose_name='Description')),
                ('name', models.CharField(blank=True, default='', help_text='The name of the item.', max_length=255, null=True, verbose_name='Name')),
                ('url', models.URLField(blank=True, help_text='URL of the item.', null=True, verbose_name='URL')),
                ('area_served', models.CharField(blank=True, help_text='The geographic area where a service or offered item is provided.', max_length=127, null=True, verbose_name='Area Served')),
                ('available_language', models.CharField(blank=True, help_text='A language someone may use with or at the item, service or place. Please use one of the language codes from the <a href="https://tools.ietf.org/html/bcp47">IETF BCP 47 standard</a>.', max_length=127, null=True, verbose_name='Available Language')),
                ('contact_type', models.CharField(blank=True, help_text='A person or organization can have different contact points, for different purposes. For example, a sales contact point, a PR contact point and so on. This property is used to specify the kind of contact point.', max_length=127, null=True, verbose_name='Contact Type')),
                ('email', models.EmailField(blank=True, help_text='Email address.', max_length=254, null=True, verbose_name='Email')),
                ('fax_number', models.CharField(blank=True, help_text='The fax number.', max_length=31, null=True, verbose_name='Fax Number')),
                ('product_supported', models.CharField(blank=True, default='', help_text='The product or service this support contact point is related to (such as product support for a particular product line). This can be a specific product or product line (e.g. "iPhone") or a general category of products or services (e.g. "smartphones").', max_length=31, null=True, verbose_name='Product Supported')),
                ('telephone', models.CharField(blank=True, default='', help_text='The telephone number.', max_length=31, null=True, verbose_name='Telephone')),
                ('mobile', models.CharField(blank=True, db_index=True, help_text='The mobile telephone number.', max_length=31, null=True, verbose_name='Mobile')),
                ('address_country', models.CharField(help_text='The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.', max_length=127, verbose_name='Address Country')),
                ('address_locality', models.CharField(help_text='The locality. For example, Mountain View.', max_length=127, verbose_name='Address Locaility')),
                ('address_region', models.CharField(help_text='The region. For example, CA.', max_length=127, verbose_name='Address Region')),
                ('post_office_box_number', models.CharField(blank=True, help_text='Apartment, suite, unit, building, floor, etc.', max_length=255, null=True, verbose_name='Post Office Box Number')),
                ('postal_code', models.CharField(blank=True, db_index=True, help_text='The postal code. For example, 94043.', max_length=127, null=True, verbose_name='Postal Code')),
                ('street_address', models.CharField(help_text='The street address. For example, 1600 Amphitheatre Pkwy.', max_length=255, verbose_name='Street Address')),
                ('street_address_extra', models.CharField(blank=True, help_text='Apartment, suite, unit, building, floor, etc.', max_length=255, null=True, verbose_name='Street Address (Extra Line)')),
                ('elevation', models.FloatField(blank=True, help_text='The elevation of a location (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).', null=True, verbose_name='Elevation')),
                ('latitude', models.DecimalField(blank=True, decimal_places=3, help_text='The latitude of a location. For example 37.42242 (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).', max_digits=8, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=3, help_text='The longitude of a location. For example -122.08585 (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).', max_digits=8, null=True, verbose_name='Longitude')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, help_text='A longitude and latitude coordinates of this location.', null=True, srid=4326, verbose_name='Location')),
                ('naics', models.CharField(blank=True, help_text='The North American Industry Classification System (NAICS) code for a particular organization or business person.', max_length=15, null=True, verbose_name='NAICS')),
                ('hours_available', models.ManyToManyField(blank=True, help_text='The hours during which this service or contact is available.', related_name='tenant_foundation_organization_contact_point_hours_available_related', to='tenant_foundation.OpeningHoursSpecification')),
                ('owner', models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_organization_abstract_thing_owner_related', to=settings.AUTH_USER_MODEL)),
                ('parent_organization', models.ForeignKey(blank=True, help_text='The larger organization that this organization is a sub-organization of', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_organization_parent_organization_related', to='tenant_foundation.Organization')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
                'db_table': 'o55_organizations',
            },
        ),
    ]
