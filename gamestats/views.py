from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from .models import GameStats as GS
from playerstats.models import PlayerStatistics as PS
from helpers import flatten_dict
import pandas as pd
from game.models import Season
from game.forms import SeasonSearchForm


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


class GameStatsList(FormMixin, ListView):
    """Display team ranking. Teams are sorted by total points."""
    model = GS
    context_object_name = 'gamestats'
    form_class = SeasonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats_fields_meta = PS.get_stats_fields_meta()
        stats_fields_verbose_names = flatten_dict(stats_fields_meta,
                                                  'verbose_name')

        # Create general team ranking or for a certain season
        season = self.request.GET.get('season', None)
        game_stats = GS.get_game_stats(season=season)

        ranking = create_ranking(game_stats)
        ranking.rename(columns=stats_fields_verbose_names, inplace=True)

        context['ranking'] = ranking.to_dict('records')

        additional_legend = {
            'WO_win': {'verbose_name': 'W/O W', 'help_text': 'Wygrane walkowerem'},
            'WO_lost': {'verbose_name': 'W/O P', 'help_text': 'Przegrane walkowerem'},
        }

        context['legend'] = PS.create_legend(additional_fields=additional_legend, fields_to_remove=['time'])
        context['year'] = season

        return context
