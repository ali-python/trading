# Generated by Django 2.2.6 on 2019-10-24 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking_system', '0003_auto_20191024_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankdetail',
            name='customer',
        ),
    ]
