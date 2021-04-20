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

    shot_1_pts_ok = models.PositiveIntegerField(default=0, verbose_name="RZ1 O")
    shot_1_pts_total = models.PositiveIntegerField(default=0, verbose_name="RZ1 T")
    shot_2_pts_ok = models.PositiveIntegerField(default=0, verbose_name="RZ2 O")
    shot_2_pts_total = models.PositiveIntegerField(default=0, verbose_name="RZ2 T")
    shot_3_pts_ok = models.PositiveIntegerField(default=0, verbose_name="RZ2 O")
    shot_3_pts_total = models.PositiveIntegerField(default=0, verbose_name="RZ3 T")

    reb_def = models.PositiveIntegerField(default=0, verbose_name="ZB D")
    reb_off = models.PositiveIntegerField(default=0, verbose_name="ZB O")
    ast = models.PositiveIntegerField(default=0, verbose_name="AS")
    stl = models.PositiveIntegerField(default=0, verbose_name="PR")
    blck = models.PositiveIntegerField(default=0, verbose_name="BL")
    ball_loos = models.PositiveIntegerField(default=0, verbose_name="ST")
    foul_def = models.PositiveIntegerField(default=0, verbose_name="FA DF")
    foul_off = models.PositiveIntegerField(default=0, verbose_name="FA OF")
    foul_unsport = models.PositiveIntegerField(default=0, verbose_name="FA N")
    foul_tech = models.PositiveIntegerField(default=0, verbose_name="FA T")
    foul_disq = models.PositiveIntegerField(default=0, verbose_name="FA D")

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    time = models.PositiveIntegerField(default=0)

    @classmethod
    def get_stats_field_names(cls):
        """Return stats related fields as a dict - { field: verbose_name }."""
        non_stats_fields = ['id', 'player_id', 'game_id', 'player', 'game']  # Unnecesary fields
        all_fields = cls.get_playerstats_names_and_verbose()
        stat_fields = {k: v for k, v in all_fields.items()
                       if k not in non_stats_fields}

        return stat_fields

    @classmethod
    def get_playerstats_names_and_verbose(cls):
        """Return model field names with corresponding verbose names."""
        model_meta = cls._meta.get_fields()
        verbose_names = {}

        for field in model_meta:
            verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_game_statistics(self):
        """Return player game statistics as a dictionary."""
        stat_fields = self.get_stats_field_names()

        stats = {}
        for stat in stat_fields:
            stats[stat] = getattr(self, stat)

        return stats

    @property
    def get_total_points(self):
        """Get total player score for the specific game."""
        return self.shot_1_pts_ok + self.shot_2_pts_ok + self.shot_3_pts_ok

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
                    player__team__name=self.player.team.name) \
            .exclude(id=self.id) \
            .count()

        if num_of_assigned_team_stats == PlayerStatistics.MAX_PLAYER_STATS_PER_GAME / 2:
            raise ValidationError(
                f'Wybrany mecz posiada już przypisaną maksymalną liczbę '
                f'statystyk dla tej drużyny wynoszącą '
                f'{int(PlayerStatistics.MAX_PLAYER_STATS_PER_GAME / 2)}.'
            )

        # One game = max 4 player statistics
        num_of_assigned_stats = PlayerStatistics.objects \
            .filter(game__id=self.game.id) \
            .exclude(id=self.id) \
            .count()

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

