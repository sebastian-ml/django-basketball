from django.core.exceptions import ValidationError
from django.db import models
from mysite.models import Player
from helpers import get_model_fields_meta_info, flatten_dict
from game.models import Game
import pandas as pd


class PlayerStatistics(models.Model):
    """
    Store player statistics.
    Each statistics must be assigned to one game.
    It's not possible to assign statistics if the game ended by forfeit.
    """
    MAX_PLAYER_STATS_PER_GAME = 4  # One game can have max 4 player statistics.

    shot_1_pts_ok = models.PositiveIntegerField(default=0, verbose_name="RZ1 O", help_text='Rzuty celne za 1 pkt')
    shot_1_pts_total = models.PositiveIntegerField(default=0, verbose_name="RZ1 T", help_text='Rzuty ogółem za 1 pkt')
    shot_2_pts_ok = models.PositiveIntegerField(default=0, verbose_name="RZ2 O", help_text='Rzuty celne za 2 pkt')
    shot_2_pts_total = models.PositiveIntegerField(default=0, verbose_name="RZ2 T", help_text='Rzuty ogółem za 2 pkt')
    shot_3_pts_ok = models.PositiveIntegerField(default=0, verbose_name="RZ3 O", help_text='Rzuty celne za 3 pkt')
    shot_3_pts_total = models.PositiveIntegerField(default=0, verbose_name="RZ3 T", help_text='Rzuty ogółem za 3 pkt')

    reb_def = models.PositiveIntegerField(default=0, verbose_name="ZB D", help_text='Zbiórki obrona')
    reb_off = models.PositiveIntegerField(default=0, verbose_name="ZB O", help_text='Zbiórki atak')
    ast = models.PositiveIntegerField(default=0, verbose_name="AS", help_text='Asysty')
    stl = models.PositiveIntegerField(default=0, verbose_name="PR", help_text='Przechwyty')
    blck = models.PositiveIntegerField(default=0, verbose_name="BL", help_text='Bloki')
    ball_loos = models.PositiveIntegerField(default=0, verbose_name="ST", help_text='Straty')
    foul_def = models.PositiveIntegerField(default=0, verbose_name="FA DF", help_text='Faule defensywne')
    foul_off = models.PositiveIntegerField(default=0, verbose_name="FA OF", help_text='Faule ofensywne')
    foul_unsport = models.PositiveIntegerField(default=0, verbose_name="FA N", help_text='Faule niesportowe')
    foul_tech = models.PositiveIntegerField(default=0, verbose_name="FA T", help_text='Faule techniczne')
    foul_disq = models.PositiveIntegerField(default=0, verbose_name="FA D", help_text='Faule dyskwalifikujące')
    time = models.PositiveIntegerField(default=0, verbose_name='T', help_text='Czas na boisku')

    player = models.ForeignKey(Player, on_delete=models.CASCADE, help_text='Gracz')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, help_text='Mecz')

    @classmethod
    def get_stats_fields_meta(cls):
        """
        Get stats fields meta information. Remove unnecesary fields.

        Return:
        field_names = {
                'field_name': {
                    'verbose_name': 'field_verbose_name',
                    'help_text': 'field_help_text',
                }
            }
        """
        stats_fields_meta_info = get_model_fields_meta_info(cls,
                                                            'verbose_name',
                                                            'help_text')

        unnecesary_fields = ['id', 'player', 'game']
        for field_name in unnecesary_fields:
            del stats_fields_meta_info[field_name]

        return stats_fields_meta_info

    @classmethod
    def create_legend(cls, additional_fields=None, fields_to_remove=None):
        """Create statistics legend."""
        legend = cls.get_stats_fields_meta()

        if additional_fields:
            legend = {**legend, **additional_fields}

        if fields_to_remove:
            for field in fields_to_remove:
                del legend[field]

        return legend

    @classmethod
    def get_stats_field_names(cls):
        """Return stats related fields as a dict - { field: verbose_name }."""
        non_stats_fields = ['id', 'player_id', 'game_id', 'player', 'game']  # Unnecesary fields
        all_fields = get_model_fields_meta_info(cls, 'verbose_name')
        all_fields = flatten_dict(all_fields, 'verbose_name')
        stat_fields = {k: v for k, v in all_fields.items()
                       if k not in non_stats_fields}

        return stat_fields

    @classmethod
    def get_player_ranking(cls, season=None):
        """Get aggregated player stats. Return as pandas df"""
        player_stats = cls.objects.all()

        if season == 'Wszystkie':
            season = None

        if season:
            player_stats = cls.objects.filter(game__season__year=season)

        # Get field names and extend by needed additional fields
        field_names = list(player_stats.values()[0].keys())
        field_names.extend(
            ('player__first_name', 'player__last_name', 'player__team')
        )

        # Calculate aggr stats for each player
        player_stats_with_teams = player_stats.values(*field_names)

        df = pd.DataFrame(list(player_stats_with_teams))
        df['game_counter'] = 1

        stats = df.groupby(
            ['player_id', 'player__first_name', 'player__last_name', 'player__team'],
            as_index=False
        ).sum()

        return stats

    @classmethod
    def get_clean_player_ranking(cls, colnames, season):
        """Rename colnames and delete unnecesary columns.

        Keyword arguments:
        ranking -- player ranking (as pandas df)
        colnames -- dictionary with old and new colnames. Must be in the following format:
        {"col1_old_name": "col1_new_name", "col2_old_name": "col2_new_name"}
        """
        ranking = cls.get_player_ranking(season)

        all_cols = {**colnames, 'player__first_name': 'Imię',
                    'player__last_name': 'Nazwisko', 'player__team': 'Drużyna',
                    'time': 'T','game_counter': 'Mecze'}

        ranking.rename(columns=all_cols, inplace=True)
        ranking.drop(columns=['game_id', 'id', 'player_id'], inplace=True)
        ranking.sort_values(by='RZ1 O', ascending=False, inplace=True)
        ranking.insert(0, '#', range(1, len(ranking.index) + 1))

        return ranking

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

