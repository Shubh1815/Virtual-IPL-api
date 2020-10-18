# Generated by Django 3.1.2 on 2020-10-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201016_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='rating',
        ),
        migrations.AddField(
            model_name='team',
            name='budget',
            field=models.FloatField(default=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='player_type',
            field=models.CharField(choices=[('All Rounder', 'All Rounder'), ('Batsmen', 'Batsmen'), ('Spin Bowler', 'Spin Bowler'), ('Pace Bowler', 'Pace Bowler'), ('Wicket Keeper', 'Wicket Keeper')], max_length=15),
        ),
    ]
