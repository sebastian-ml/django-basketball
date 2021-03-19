from django.core.exceptions import ValidationError
from django.db import models
from mysite.models import Player
from game.models import Game


class PlayerStatistics(models.Model):
    q1_foul = models.IntegerField()
    q2_foul = models.IntegerField()
    q3_foul = models.IntegerField()
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['player', 'game']
        db_table = 'player_statistics'

    def clean(self):
        # Check if the selected player belongs to the team_1 or team_2 in the choosen game
        if (self.player.team.name not in
                [self.game.team_1.name, self.game.team_2.name]):

            raise ValidationError(
                f'Należy wybrać gracza z drużyny '
                f'{self.game.team_2.name} lub {self.game.team_1.name}!'
            )

        # Forbid adding player statistics if the game was ended by forfeit
        if self.game.forfeit is not None:
            raise ValidationError(
                'Nie można dodać statystyk gracza do meczu zakończonego walkowerem.'
            )

    def __str__(self):
        return f'{self.player} | {self.game}'
