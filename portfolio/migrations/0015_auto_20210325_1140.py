# Generated by Django 3.1.7 on 2021-03-25 02:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0014_auto_20210325_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 40, 5, 515429, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='corp',
            name='updated_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='mycorp',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 40, 5, 516930, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='myport',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 40, 5, 516006, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 40, 5, 513997, tzinfo=utc)),
        ),
    ]
