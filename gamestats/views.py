from django.views.generic import ListView
from .models import GameStats as GS


def get_game_stats(season=None, game_done=True, game_done_stats_amount=4):
    """Return game stats for all seasons or for the specific season.

    Keyword arguments:
    season -- the season year, e.g. 2021
    game_done -- the game status - if True get only games that has all needed stats
    game_done_stats_amount -- the required number of stats to mark the game as done
    """
    if season is None:
        game_stats = GS.objects.all()
    else:
        game_stats = GS.objects.filter(game__season__year=season)

    if game_done:
        done_games_ids = [game.id for game in game_stats if game.game_is_over(game_done_stats_amount)]
        return game_stats.filter(id__in=done_games_ids)
    else:
        return game_stats


def get_team_names(game_stats):
    """Return a queryset with distinct team names from the given game_stats."""
    return game_stats \
        .values_list('team', flat=True) \
        .distinct() \
        .order_by()


def create_team_ranking(game_stats):
    """Create team ranking from the given game stats."""
    stats = ['wins', 'losses']
    teams = get_team_names(game_stats)

    '''
    Create an empty dict for all teams. Example: ranking = {
    'team1': {
        'wins': 2,
        'losses': 3,
    }
    '''
    ranking = dict.fromkeys(teams, {})
    for team, v in ranking.items():
        ranking[team] = dict.fromkeys(stats, 0)

    for teamstats in game_stats:
        team = teamstats.team.name

        if teamstats.is_winner:
            ranking[team]['wins'] += 1
        if not teamstats.is_winner:
            ranking[team]['losses'] += 1

    return ranking


class GameStatsList(ListView):
    """Display team ranking. Teams are sorted by total points."""
    model = GS
    context_object_name = 'gamestats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        game_stats = get_game_stats(season=2021)
        context['test'] = create_team_ranking(game_stats)

        return context
