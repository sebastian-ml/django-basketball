from django.views.generic import ListView
from .models import GameStats as GS
from playerstats.models import PlayerStatistics as PS
from helpers import get_model_fields_meta_info, flatten_dict
import pandas as pd


def create_ranking(game_stats):
    """
    Calculate total points from the given game stats. Sort by number of wins.
    Return as a pandas df, each row - 1 team.
    """
    ranking = []

    for game_stat in game_stats:
        game_team_stats = {'Drużyna': game_stat.team.name,
                           'Wygrane': game_stat.is_winner,
                           'Zagrane mecze': 1,
                           'W/O W': game_stat.is_forfeit_winner,
                           'W/O P': game_stat.is_forfeit_looser}

        game_total_team_pts = game_stat.get_game_team_stats()
        game_team_stats.update(game_total_team_pts)

        ranking.append(game_team_stats)

    df = pd.DataFrame(ranking)
    df = df.groupby(['Drużyna'], as_index=False).sum()
    df.sort_values(by='Wygrane', ascending=False, inplace=True)
    df.insert(0, '#', range(1, len(df.index) + 1))

    return df


class GameStatsList(ListView):
    """Display team ranking. Teams are sorted by total points."""
    model = GS
    context_object_name = 'gamestats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create general team ranking or for a certain season
        season = self.kwargs.get('year', None)

        game_stats = GS.get_game_stats(season=season)
        stats_field_verbose = get_model_fields_meta_info(PS, 'verbose_name')
        stats_field_verbose = flatten_dict(stats_field_verbose, 'verbose_name')

        ranking = create_ranking(game_stats)
        ranking.rename(columns=stats_field_verbose, inplace=True)

        context['ranking'] = ranking.to_dict('records')

        return context
