# Generated by Django 4.0.2 on 2022-02-11 09:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_shoes_hash_shoes_txid_alter_profile_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 11, 10, 58, 15, 644508)),
        ),
        migrations.AlterField(
            model_name='shoes',
            name='end_auction',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 11, 10, 58, 15, 645510)),
        ),
    ]
