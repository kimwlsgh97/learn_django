# Generated by Django 3.1.7 on 2021-03-30 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0033_auto_20210330_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myport',
            name='port_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sector',
            name='sector_price',
            field=models.IntegerField(default=0),
        ),
    ]
