# Generated by Django 3.2.10 on 2021-12-18 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_plans_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='contract',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='contracts.plans'),
        ),
    ]