# Generated by Django 3.1.7 on 2021-03-31 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0035_auto_20210330_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycorp',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
