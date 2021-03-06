# Generated by Django 3.2.10 on 2021-12-28 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0015_edit_solarschedule_events_choices'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(blank=True, choices=[('BITCOIN', 'Bitcon'), ('ETHEREUM', 'Ethereum'), ('LITECOIN', 'Litecoin')], default='BITCOIN', max_length=60)),
                ('address', models.CharField(max_length=250)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('verified', models.BooleanField(default=False)),
                ('exh_rate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='deprate', to='wallet.exchangerate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraw', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Withdrawal',
                'verbose_name_plural': 'Withdrawals',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('bitcoin_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('litecoin_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('ethereum_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('recent_balance_added', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('total_investment', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('exh_rate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exchrate', to='wallet.exchangerate')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wallet Balance',
                'verbose_name_plural': 'Wallet Balances',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(blank=True, choices=[('BITCOIN', 'Bitcon'), ('ETHEREUM', 'Ethereum'), ('LITECOIN', 'Litecoin')], default='BITCOIN', max_length=60)),
                ('type', models.CharField(blank=True, choices=[('Invest', 'Invest'), ('Withdraw', 'Withdraw'), ('ROI', 'ROI')], max_length=60)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('verified', models.BooleanField(default=False)),
                ('exh_rate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tranrate', to='wallet.exchangerate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(blank=True, choices=[('BITCOIN', 'Bitcon'), ('ETHEREUM', 'Ethereum'), ('LITECOIN', 'Litecoin')], default='BITCOIN', max_length=60)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('verified', models.BooleanField(default=False)),
                ('exh_rate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='invrate', to='wallet.exchangerate')),
                ('roitask', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deposittask', to='django_celery_beat.periodictask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invest', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Deposit',
                'verbose_name_plural': 'Deposits',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
    ]
