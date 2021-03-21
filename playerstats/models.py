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

    q1_shot_1_pts_ok = models.PositiveIntegerField(default=0)
    q1_shot_1_pts_total = models.PositiveIntegerField(default=0)
    q2_shot_1_pts_ok = models.PositiveIntegerField(default=0)
    q2_shot_1_pts_total = models.PositiveIntegerField(default=0)
    q3_shot_1_pts_ok = models.PositiveIntegerField(default=0)
    q3_shot_1_pts_total = models.PositiveIntegerField(default=0)
    q4_shot_1_pts_ok = models.PositiveIntegerField(default=0)
    q4_shot_1_pts_total = models.PositiveIntegerField(default=0)

    q1_shot_2_pts_ok = models.PositiveIntegerField(default=0)
    q1_shot_2_pts_total = models.PositiveIntegerField(default=0)
    q2_shot_2_pts_ok = models.PositiveIntegerField(default=0)
    q2_shot_2_pts_total = models.PositiveIntegerField(default=0)
    q3_shot_2_pts_ok = models.PositiveIntegerField(default=0)
    q3_shot_2_pts_total = models.PositiveIntegerField(default=0)
    q4_shot_2_pts_ok = models.PositiveIntegerField(default=0)
    q4_shot_2_pts_total = models.PositiveIntegerField(default=0)

    q1_shot_3_pts_ok = models.PositiveIntegerField(default=0)
    q1_shot_3_pts_total = models.PositiveIntegerField(default=0)
    q2_shot_3_pts_ok = models.PositiveIntegerField(default=0)
    q2_shot_3_pts_total = models.PositiveIntegerField(default=0)
    q3_shot_3_pts_ok = models.PositiveIntegerField(default=0)
    q3_shot_3_pts_total = models.PositiveIntegerField(default=0)
    q4_shot_3_pts_ok = models.PositiveIntegerField(default=0)
    q4_shot_3_pts_total = models.PositiveIntegerField(default=0)

    q1_reb_def = models.PositiveIntegerField(default=0)
    q2_reb_def = models.PositiveIntegerField(default=0)
    q3_reb_def = models.PositiveIntegerField(default=0)
    q4_reb_def = models.PositiveIntegerField(default=0)

    q1_reb_off = models.PositiveIntegerField(default=0)
    q2_reb_off = models.PositiveIntegerField(default=0)
    q3_reb_off = models.PositiveIntegerField(default=0)
    q4_reb_off = models.PositiveIntegerField(default=0)

    q1_ast = models.PositiveIntegerField(default=0)
    q2_ast = models.PositiveIntegerField(default=0)
    q3_ast = models.PositiveIntegerField(default=0)
    q4_ast = models.PositiveIntegerField(default=0)

    q1_stl = models.PositiveIntegerField(default=0)
    q2_stl = models.PositiveIntegerField(default=0)
    q3_stl = models.PositiveIntegerField(default=0)
    q4_stl = models.PositiveIntegerField(default=0)

    q1_blck = models.PositiveIntegerField(default=0)
    q2_blck = models.PositiveIntegerField(default=0)
    q3_blck = models.PositiveIntegerField(default=0)
    q4_blck = models.PositiveIntegerField(default=0)

    q1_ball_loos = models.PositiveIntegerField(default=0)
    q2_ball_loos = models.PositiveIntegerField(default=0)
    q3_ball_loos = models.PositiveIntegerField(default=0)
    q4_ball_loos = models.PositiveIntegerField(default=0)

    q1_foul_def = models.PositiveIntegerField(default=0)
    q2_foul_def = models.PositiveIntegerField(default=0)
    q3_foul_def = models.PositiveIntegerField(default=0)
    q4_foul_def = models.PositiveIntegerField(default=0)

    q1_foul_off = models.PositiveIntegerField(default=0)
    q2_foul_off = models.PositiveIntegerField(default=0)
    q3_foul_off = models.PositiveIntegerField(default=0)
    q4_foul_off = models.PositiveIntegerField(default=0)

    q1_foul_unsport = models.PositiveIntegerField(default=0)
    q2_foul_unsport = models.PositiveIntegerField(default=0)
    q3_foul_unsport = models.PositiveIntegerField(default=0)
    q4_foul_unsport = models.PositiveIntegerField(default=0)

    q1_foul_tech = models.PositiveIntegerField(default=0)
    q2_foul_tech = models.PositiveIntegerField(default=0)
    q3_foul_tech = models.PositiveIntegerField(default=0)
    q4_foul_tech = models.PositiveIntegerField(default=0)

    q1_foul_disq = models.PositiveIntegerField(default=0)
    q2_foul_disq = models.PositiveIntegerField(default=0)
    q3_foul_disq = models.PositiveIntegerField(default=0)
    q4_foul_disq = models.PositiveIntegerField(default=0)

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    time = models.PositiveIntegerField(default=0)

    @property
    def get_total_points(self):
        """Get total player score for the specific game."""
        total_1_pts_shots = sum([self.q1_shot_1_pts_ok,
                                 self.q2_shot_1_pts_ok,
                                 self.q3_shot_1_pts_ok,
                                 self.q4_shot_1_pts_ok])

        total_2_pts_shots = sum([self.q1_shot_2_pts_ok,
                                 self.q2_shot_2_pts_ok,
                                 self.q3_shot_2_pts_ok,
                                 self.q4_shot_2_pts_ok])

        total_3_pts_shots = sum([self.q1_shot_3_pts_ok,
                                 self.q2_shot_3_pts_ok,
                                 self.q3_shot_3_pts_ok,
                                 self.q4_shot_3_pts_ok])

        return (total_1_pts_shots
                + (total_2_pts_shots * 2)
                + (total_3_pts_shots * 3))

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

    class Meta:
        unique_together = ['player', 'game']
        db_table = 'player_statistics'
        ordering = ['-game__id', '-player__team']

    def __str__(self):
        return f'{self.player} | {self.game}'

