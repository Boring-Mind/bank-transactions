# Generated by Django 3.1 on 2020-09-01 15:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200831_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=16, validators=[django.core.validators.MinValueValidator]),
        ),
    ]
