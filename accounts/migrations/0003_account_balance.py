# Generated by Django 3.1 on 2020-08-31 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200823_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=16),
            preserve_default=False,
        ),
    ]
