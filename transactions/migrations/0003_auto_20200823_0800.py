# Generated by Django 3.1 on 2020-08-23 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20200819_0657'),
        ('transactions', '0002_auto_20200823_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='receiver_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver_transaction', to='clients.account'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='sender_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender_transaction', to='clients.account'),
        ),
    ]