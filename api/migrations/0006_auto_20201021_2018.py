# Generated by Django 3.1.2 on 2020-10-21 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201021_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
