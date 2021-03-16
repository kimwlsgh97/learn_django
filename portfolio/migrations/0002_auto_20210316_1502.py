# Generated by Django 3.1.7 on 2021-03-16 06:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corp',
            fields=[
                ('corp_id', models.IntegerField(primary_key=True, serialize=False)),
                ('corp_name', models.CharField(max_length=100, unique=True)),
                ('stock_code', models.IntegerField(null=True)),
                ('stock_price', models.IntegerField(null=True)),
                ('stock_num', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 6, 2, 24, 129639, tzinfo=utc)),
        ),
    ]
