# Generated by Django 3.2.10 on 2021-12-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_alter_contract_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='expires',
            field=models.DateField(blank=True, null=True),
        ),
    ]
