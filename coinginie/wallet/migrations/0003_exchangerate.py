# Generated by Django 3.2.10 on 2021-12-17 08:10

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20211216_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('bitcoin_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('litecoin_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('ethereum_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
            ],
            options={
                'verbose_name': 'Exchange Rate',
                'verbose_name_plural': 'Exchange Rates',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
    ]
