from datetime import datetime
from django.db import models
from mysite.models import Team


class Season(models.Model):
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.year} season'


class Game(models.Model):
    date = models.DateField()
    team_1 = models.ForeignKey(Team,
                               on_delete=models.CASCADE,
                               related_name='home_team')
    team_2 = models.ForeignKey(Team,
                               on_delete=models.CASCADE,
                               related_name='away_team')
    season = models.ForeignKey(Season,
                               on_delete=models.CASCADE)

    class Meta:
        unique_together = ['team_1', 'team_2', 'date']

    def __str__(self):
        return f'{self.team_1} vs {self.team_2} | {self.date}'
