# Generated by Django 3.1.7 on 2021-03-19 08:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20210318_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 19, 8, 31, 57, 754945, tzinfo=utc)),
        ),
    ]