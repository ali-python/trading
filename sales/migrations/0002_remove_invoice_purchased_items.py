# Generated by Django 2.2.6 on 2019-10-22 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='purchased_items',
        ),
    ]
