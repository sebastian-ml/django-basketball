from django.core.exceptions import ValidationError
from django.db import models
from mysite.models import Player
from game.models import Game


class PlayerStatistics(models.Model):
    """
    Store player statistics.
    Each statistics must be assigned to one game.
    It's not possible to assign statistics if the game ended by forfeit.
    """
    MAX_PLAYER_STATS_PER_GAME = 4  # One game can have max 4 player statistics.

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
        ordering = ['-game__id', '-player__team']

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

        # One game = max 2 player statistics from one team
        num_of_assigned_team_stats = PlayerStatistics.objects \
            .filter(game__id=self.game.id,
                    player__team__name=self.player.team.name).count()

        if num_of_assigned_team_stats == PlayerStatistics.MAX_PLAYER_STATS_PER_GAME / 2:
            raise ValidationError(
                f'Wybrany mecz posiada już przypisaną maksymalną liczbę '
                f'statystyk dla tej drużyny wynoszącą '
                f'{int(PlayerStatistics.MAX_PLAYER_STATS_PER_GAME / 2)}.'
            )

        # One game = max 4 player statistics
        num_of_assigned_stats = PlayerStatistics.objects \
            .filter(game__id=self.game.id).count()

        if num_of_assigned_stats == PlayerStatistics.MAX_PLAYER_STATS_PER_GAME:
            raise ValidationError(
                f'Nie można dodać więcej statystyk do tego meczu. '
                f'Wybrany mecz posiada już przypisane statystyki dla '
                f'{PlayerStatistics.MAX_PLAYER_STATS_PER_GAME} graczy.'
            )

    def __str__(self):
        return f'{self.player} | {self.game}'
