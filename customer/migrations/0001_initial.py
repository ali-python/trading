# Generated by Django 2.2.6 on 2019-10-16 08:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('father_name', models.CharField(blank=True, max_length=200, null=True)),
                ('cnic', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('alternate_mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('resident', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]
