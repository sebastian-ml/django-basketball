from django.core.exceptions import ValidationError
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return f'{self.name}'


class Player(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}' \
               f' ({self.team.name})'


class PlayerStatistics(models.Model):
    q1_foul = models.IntegerField()
    q2_foul = models.IntegerField()
    q3_foul = models.IntegerField()
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        'game.Game',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['player', 'game']

    def clean(self):
        # Check if the selected player belongs to the team_1 or team_2 in the choosen game
        if (self.player.team.name not in
                [self.game.team_1.name, self.game.team_2.name]):

            raise ValidationError(
                f'Należy wybrać gracza z drużyny '
                f'{self.game.team_2.name} lub {self.game.team_1.name}!'
            )

    def __str__(self):
        return f'{self.player} | {self.game}'
