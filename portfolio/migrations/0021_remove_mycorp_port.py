# Generated by Django 3.1.7 on 2021-03-26 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0020_auto_20210326_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycorp',
            name='port',
        ),
    ]
