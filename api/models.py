from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Team(models.Model):
    team_no = models.IntegerField(primary_key=True)
    budget = models.FloatField()

    def __str__(self):
        return str(self.team_no)

class Player(models.Model):
    player_name = models.CharField(max_length=100)
    player_type = models.CharField(max_length=15,
        choices=[
            ('All Rounder', 'All Rounder'),
            ('Batsmen', 'Batsmen'),
            ('Spinners', 'Spin Bowler'),
            ('Pace Bowler', 'Pace Bowler'),
            ('WK-Batsman', 'Wicket Keeper')
        ]
    )
    player_rating = models.FloatField()
    price = models.FloatField(default=0, null=True)

    team = models.ForeignKey(Team, related_name="players", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.player_name

class Top10(models.Model):
    top10 = ArrayField(
        models.JSONField(),
        size=10,
        default=list,
        blank=True,
    )
