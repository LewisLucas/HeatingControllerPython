# Generated by Django 5.1.6 on 2025-02-26 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatingApp', '0002_rename_readvalues_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timer',
            name='length',
        ),
        migrations.AddField(
            model_name='info',
            name='target_temperature',
            field=models.FloatField(default=10),
        ),
        migrations.AlterField(
            model_name='info',
            name='humidity',
            field=models.FloatField(default=50),
        ),
        migrations.AlterField(
            model_name='info',
            name='temperature',
            field=models.FloatField(default=21),
        ),
    ]
