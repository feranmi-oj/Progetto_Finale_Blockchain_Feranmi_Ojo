# Generated by Django 4.0.2 on 2022-02-08 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='end_auction',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 8, 11, 52, 4, 216373)),
        ),
    ]
