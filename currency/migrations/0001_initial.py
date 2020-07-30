# Generated by Django 3.0.8 on 2020-07-30 13:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=3, unique=True)),
                ('full_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0, message='Currency exchange rate cannot be less that zero')])),
                ('currency_receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver_rate', to='currency.Currency')),
                ('currency_sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender_rate', to='currency.Currency')),
            ],
        ),
    ]