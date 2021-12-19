# Generated by Django 3.2.10 on 2021-12-15 16:04

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211215_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='broker',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]