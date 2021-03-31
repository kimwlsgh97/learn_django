# Generated by Django 3.1.7 on 2021-03-25 02:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_auto_20210325_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='corp',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 24, 10, 613770, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='mycorp',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 24, 10, 615397, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='myport',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 24, 10, 614442, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 25, 2, 24, 10, 613101, tzinfo=utc)),
        ),
    ]
