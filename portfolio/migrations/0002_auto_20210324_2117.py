# Generated by Django 3.1.7 on 2021-03-24 12:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 24, 12, 17, 35, 500902, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='mycorp',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 24, 12, 17, 35, 503368, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='myport',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 24, 12, 17, 35, 501909, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 24, 12, 17, 35, 500043, tzinfo=utc)),
        ),
    ]
