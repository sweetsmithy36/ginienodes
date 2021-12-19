# Generated by Django 3.2.10 on 2021-12-15 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_consent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='consent',
            field=models.BooleanField(default=False, help_text="</br>By signing up you consent to our <a href='/privacy/'>privacy agreement</a> and <a href='/terms/'>terms of use</a>."),
        ),
    ]
