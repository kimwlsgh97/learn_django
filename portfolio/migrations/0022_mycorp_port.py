# Generated by Django 3.1.7 on 2021-03-26 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0021_remove_mycorp_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycorp',
            name='port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corps', to='portfolio.myport'),
        ),
    ]