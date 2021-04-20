from django.views.generic import ListView
from .models import GameStats as GS
from playerstats.models import PlayerStatistics as PS
from helpers import get_model_fields_with_verbose_names
import pandas as pd


def get_game_stats(season=None, game_done=True, game_done_stats_amount=4):
    """Return game stats for all seasons or for the specific season.

    Keyword arguments:
    season -- the season year, e.g. 2021
    game_done -- the game status - if True get only games that has all needed stats
    game_done_stats_amount -- the required number of stats to mark the game as done
    """
    game_stats = GS.objects.all()

    if season is not None:
        game_stats = GS.objects.filter(game__season__year=season)

    if game_done:
        done_games_ids = [game.id for game in game_stats if game.game_is_over(game_done_stats_amount)]
        return game_stats.filter(id__in=done_games_ids)
    else:
        return game_stats


def create_ranking(game_stats):
    """
    Calculate total points from the given game stats. Sort by number of winds.
    Return as a pandas df, each row - 1 team.
    """
    ranking = []

    for game_stat in game_stats:
        game_team_stats = {'team': game_stat.team.name,
                           'winner': game_stat.is_winner,
                           'by_forfeit': game_stat.game_ended_by_forfeit}

        game_total_team_pts = game_stat.get_team_stats()
        game_team_stats.update(game_total_team_pts)

        ranking.append(game_team_stats)

    df = pd.DataFrame(ranking)
    df = df.groupby(['team'], as_index=False).sum()
    df.sort_values(by='winner', inplace=True)

    return df


class GameStatsList(ListView):
    """Display team ranking. Teams are sorted by total points."""
    model = GS
    context_object_name = 'gamestats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        game_stats = get_game_stats(season=2021)
        stats_field_verbose = get_model_fields_with_verbose_names(PS)
        headers = {**stats_field_verbose, 'team': 'Drużyna', 'winner': 'Wygrane', 'by_forfeit': 'W/O'}
        ranking = create_ranking(game_stats)
        ranking.rename(columns=headers, inplace=True)

        context['ranking'] = ranking.to_dict('records')

        return context
