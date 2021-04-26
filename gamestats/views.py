from django.views.generic import ListView
from .models import GameStats as GS
from playerstats.models import PlayerStatistics as PS
from helpers import flatten_dict, get_stats_fields_meta
import pandas as pd


def create_ranking(game_stats):
    """
    Calculate total points from the given game stats. Sort by number of wins.
    Return as a pandas df, each row - 1 team.
    """
    ranking = []

    for game_stat in game_stats:
        game_team_stats = {'Drużyna': game_stat.team.name,
                           'Mecze': 1,
                           'Wygrane': game_stat.is_winner,
                           'Przegrane': not game_stat.is_winner,
                           'W/O W': game_stat.is_forfeit_winner,
                           'W/O P': game_stat.is_forfeit_looser}

        game_total_team_pts = game_stat.get_game_team_stats()
        game_team_stats.update(game_total_team_pts)

        ranking.append(game_team_stats)

    df = pd.DataFrame(ranking)
    df = df.groupby(['Drużyna'], as_index=False).sum()
    df.sort_values(by='Wygrane', ascending=False, inplace=True)
    df.insert(0, '#', range(1, len(df.index) + 1))

    total_points = df['Wygrane'] * 2 + df['Przegrane'] - df['W/O P']
    df.insert(1, 'PKT', total_points)

    return df


class GameStatsList(ListView):
    """Display team ranking. Teams are sorted by total points."""
    model = GS
    context_object_name = 'gamestats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats_fields_meta = get_stats_fields_meta(PS)
        stats_fields_verbose_names = flatten_dict(stats_fields_meta,
                                                  'verbose_name')

        # Create general team ranking or for a certain season
        season = self.kwargs.get('year', None)
        game_stats = GS.get_game_stats(season=season)

        ranking = create_ranking(game_stats)
        ranking.rename(columns=stats_fields_verbose_names, inplace=True)

        context['ranking'] = ranking.to_dict('records')
        context['legend'] = stats_fields_meta

        return context
