from django.core.exceptions import ValidationError
from django.db import models
from mysite.models import Team


class Season(models.Model):
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'season'

    def __str__(self):
        return f'{self.year} season'


class Game(models.Model):
    """
    Create game between 2 teams.
    Allow to add info if a team lost by forfeit.
     """
    date = models.DateField()
    team_1 = models.ForeignKey(Team,
                               on_delete=models.CASCADE,
                               related_name='home_team')
    team_2 = models.ForeignKey(Team,
                               on_delete=models.CASCADE,
                               related_name='away_team')
    season = models.ForeignKey(Season,
                               on_delete=models.CASCADE)
    forfeit = models.ForeignKey(Team,
                                on_delete=models.CASCADE,
                                blank=True, null=True)

    class Meta:
        unique_together = ['team_1', 'team_2', 'date']
        db_table = 'game'

    def clean(self):
        # Do not allow to choose the same home and away team
        if self.team_2 == self.team_1:
            raise ValidationError(
                'Mecz musi być rozgrywany pomiędzy dwoma różnymi drużynami!'
            )
        # Team which lost by forfeit must be team 1 or team 2
        if self.forfeit not in [self.team_1, self.team_2]:
            raise ValidationError(
                f'Walkower można wybrać tylko dla drużyny {self.team_1} lub {self.team_2}'
            )

    def __str__(self):
        return f'{self.id}. {self.team_1} vs {self.team_2} ' \
               f'| {self.date} | season {self.season.year}'
