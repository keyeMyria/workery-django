# Generated by Django 2.0 on 2018-02-04 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_foundation', '0001_initial'),
        ('tenant_foundation', '0005_auto_20180203_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerComment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('comment', models.ForeignKey(help_text='The comment of our reference.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_customercomment_comment_related', to='tenant_foundation.Comment')),
                ('created_by', models.ForeignKey(help_text='The user whom created this comment.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_customercomment_created_by_related', to='shared_foundation.O55User')),
                ('customer', models.ForeignKey(help_text='The customer of our reference.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_customercomment_customer_related', to='tenant_foundation.Customer')),
            ],
            options={
                'verbose_name': 'Customer Comment',
                'verbose_name_plural': 'Customer Comments',
                'db_table': 'o55_customer_comments',
                'ordering': ('-created_at',),
                'permissions': (('can_get_customer_comments', 'Can get customer comments'), ('can_get_customer_comment', 'Can get customer comment'), ('can_post_customer_comment', 'Can post customer comment'), ('can_put_customer_comment', 'Can update customer comment'), ('can_delete_customer_comment', 'Can delete customer comment')),
                'default_permissions': (),
            },
        ),
        migrations.AlterField(
            model_name='ordercomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='comments',
            field=models.ManyToManyField(blank=True, help_text='The comments of this customer sorted by latest creation date..', related_name='tenant_foundation_customer_comments_related', through='tenant_foundation.CustomerComment', to='tenant_foundation.Comment'),
        ),
    ]