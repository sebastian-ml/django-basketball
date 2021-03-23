from django.core.exceptions import ValidationError
from django.db import models
from game.models import Game
from mysite.models import Team
from playerstats.models import PlayerStatistics as PS


def get_total_points(game, team):
    """Return total points for the specific game gained by specific team."""
    player_stats = PS.objects.filter(game=game, player__team=team)
    total_team_pts = sum([stat.get_total_points for stat in player_stats])

    return total_team_pts


class GameStats(models.Model):
    """
    Store team statistics related to each game.
    Each game must have only 2 instances of GameStats.
    One instance for team1, and one instance for team2.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    @property
    def get_opponent(self):
        if self.team == self.game.team_1:
            return self.game.team_2
        else:
            return self.game.team_1

    @property
    def get_score(self):
        return get_total_points(self.game, self.team)

    @property
    def get_opponent_score(self):
        return get_total_points(self.game, self.get_opponent)

    @property
    def game_ended_by_forfeit(self):
        return self.game.forfeit is not None

    @property
    def is_winner(self):
        if self.game_ended_by_forfeit:
            forfeit_team = self.game.forfeit

            return self.team != forfeit_team
        else:
            return self.get_score > self.get_opponent_score

    def game_is_over(self, expected_stats_count=4):
        """
        Check if the game has all player stats or the game ended by forfeit.

        expected_stats_count -- number of unique player stats related to the game.
        E.g. 4 means that the game must have exactly 4 player stats.
        """
        assigned_player_stats = PS.objects.filter(game=self.game).count()
        assigned_player_stats_team = PS.objects \
            .filter(game=self.game, player__team=self.team).count()

        game_has_required_stats = (
                (assigned_player_stats == expected_stats_count) and
                (assigned_player_stats_team == expected_stats_count / 2)
        )

        return game_has_required_stats or self.game_ended_by_forfeit

    def clean(self):
        # Chosen team must be same as team1 or team2 from the desired game
        if self.team not in [self.game.team_1, self.game.team_2]:
            raise ValidationError(
                f'Dla wybranej gry można przypisać statystyki drużyny '
                f'której wybrany mecz dotyczy - {self.game.team_1} lub {self.game.team_2}'
            )

    class Meta:
        db_table = 'game_stats'
        unique_together = ['team', 'game']
        ordering = ['-game']

    def __str__(self):
        return f'game: {self.game.id} team: {self.team}'
