# Generated by Django 3.1.7 on 2021-03-25 00:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_auto_20210325_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 25, 0, 20, 29, 170874, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='mycorp',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 25, 0, 20, 29, 172413, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='myport',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 25, 0, 20, 29, 171496, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 0, 20, 29, 170313, tzinfo=utc)),
        ),
    ]