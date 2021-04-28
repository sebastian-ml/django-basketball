from django.core.exceptions import ValidationError
from django.db import models
from game.models import Game
from mysite.models import Team
from playerstats.models import PlayerStatistics as PS


class GameStats(models.Model):
    """
    Store team statistics related to each game.
    Each game must have only 2 instances of GameStats.
    One instance for team1, and one instance for team2.
    """
    # Number of player stats required for game to be over
    GAME_OVER_NUMBER_OF_STATS = {
        'all': 4,
        'per_team': 2,
    }

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    @classmethod
    def get_game_stats(cls, season=None, game_done=True):
        """Return game stats for all seasons or for the specific season.

        Keyword arguments:
        season -- the season year, e.g. 2021
        game_done -- the game status - if True get only games that has all needed stats
        game_done_stats_amount -- the required number of stats to mark the game as done
        """
        game_stats = cls.objects.all()

        if season == 'Wszystkie':
            season = None

        if season:
            game_stats = cls.objects.filter(game__season__year=season)

        if game_done:
            done_games_ids = [game.id for game in game_stats if
                              game.is_game_over()]
            return game_stats.filter(id__in=done_games_ids)
        else:
            return game_stats

    @property
    def get_opponent_name(self):
        if self.team == self.game.team_1:
            return self.game.team_2
        else:
            return self.game.team_1

    @property
    def get_score(self):
        return self.get_team_points_in_game(self.team)

    @property
    def get_opponent_score(self):
        return self.get_team_points_in_game(self.get_opponent_name)

    @property
    def is_game_ended_by_forfeit(self):
        return self.game.forfeit is not None

    @property
    def is_winner(self):
        if self.is_game_ended_by_forfeit:
            forfeit_team = self.game.forfeit

            return self.team != forfeit_team
        else:
            return self.get_score > self.get_opponent_score

    @property
    def is_forfeit_winner(self):
        return self.is_winner and self.is_game_ended_by_forfeit

    @property
    def is_forfeit_looser(self):
        return (not self.is_winner) and self.is_game_ended_by_forfeit

    def get_team_points_in_game(self, team):
        """Return total points for the specific game gained by specific team."""
        player_stats = PS.objects.filter(game=self.game, player__team=team)
        total_team_pts = sum([stat.get_total_points for stat in player_stats])

        return total_team_pts

    def is_game_over(self):
        """
        Check if the game has all player stats or the game ended by forfeit.

        expected_stats_count -- number of unique player stats related to the game.
        E.g. 4 means that the game must have exactly 4 player stats.
        """
        assigned_player_stats = PS.objects.filter(game=self.game).count()
        assigned_player_stats_team = PS.objects \
            .filter(game=self.game, player__team=self.team).count()

        has_game_required_stats = (
                (assigned_player_stats == self.GAME_OVER_NUMBER_OF_STATS['all']) and
                (assigned_player_stats_team == self.GAME_OVER_NUMBER_OF_STATS['per_team'])
        )

        return self.is_game_ended_by_forfeit or has_game_required_stats

    def get_game_team_stats(self):
        """Return aggreated statistics for the specific game for the specific team."""
        stats_field_names = PS.get_stats_field_names()
        player_stats = PS.objects.filter(game=self.game, player__team=self.team)

        team_game_stats = dict.fromkeys(stats_field_names, 0)

        for stat in stats_field_names:
            for player in player_stats:
                team_game_stats[stat] += getattr(player, stat)

        return team_game_stats

    def clean(self):
        # Chosen team must be same as team1 or team2 from the desired game
        if self.team not in [self.game.team_1, self.game.team_2]:
            raise ValidationError(
                f'Dla wybranej gry można przypisać jedynie statystyki drużyny '
                f'której wybrany mecz dotyczy - {self.game.team_1} lub {self.game.team_2}'
            )

    class Meta:
        db_table = 'game_stats'
        unique_together = ['team', 'game']
        ordering = ['-game']

    def __str__(self):
        return f'game: {self.game.id} team: {self.team}'
