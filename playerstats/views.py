from .models import PlayerStatistics
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
import pandas as pd


class PlayerStatsCreate(CreateView):
    """Add player statistics which belongs to certain game."""
    model = PlayerStatistics
    fields = '__all__'
    success_url = reverse_lazy('home:player-stats-add')


def get_playerstats_names_and_verbose():
    """Return PlayerStatistics field names with corresponding verbose names."""
    model_meta = PlayerStatistics._meta.get_fields()
    verbose_names = {}

    for field in model_meta:
        verbose_names[field.name] = field.verbose_name

    return verbose_names


def get_player_ranking(year=None):
    """Get aggregated player stats. Return as pandas df"""
    player_stats = PlayerStatistics.objects.all()

    if year:
        player_stats = PlayerStatistics.objects.filter(game__season__year=year)

    # Get field names and extend by needed additional fields
    field_names = list(player_stats.values()[0].keys())
    field_names.extend(('player__first_name', 'player__last_name', 'player__team'))

    # Calculate aggr stats for each player
    df = pd.DataFrame(list(player_stats.values(*field_names)))
    stats = df.groupby(['player_id', 'player__first_name', 'player__last_name', 'player__team'], as_index=False).sum()

    return stats


def prepare_player_ranking(ranking, colnames):
    """Rename colnames and delete unnecesary columns.

    Keyword arguments:
    ranking -- player ranking (as pandas df)
    colnames -- dictionary with old and new colnames. Must be in the following format:
    {"col1_old_name": "col1_new_name", "col2_old_name": "col2_new_name"}
    """

    ranking.rename(columns=colnames, inplace=True)
    ranking.rename(
        columns={'player__first_name': 'Imię', 'player__last_name': 'Nazwisko',
                 'player__team': 'Drużyna', 'time': 'Czas', 'player_id': '#'},
        inplace=True)
    ranking.drop(columns=['game_id', 'ID'], inplace=True)

    return ranking


class PlayerStatsList(ListView):
    """Show player stats ranking list."""
    model = PlayerStatistics

    # Note: Currently it contains only fouls - will be expanded in the future
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        playerstats_verbose = get_playerstats_names_and_verbose()
        player_ranking = get_player_ranking()
        player_ranking_cleaned = prepare_player_ranking(player_ranking,
                                                        playerstats_verbose)

        context['player_ranking'] = player_ranking_cleaned.to_dict('records')

        return context


class PlayerStatsSeasonList(ListView):
    """Show player stats ranking list for a specific season."""
    model = PlayerStatistics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        playerstats_verbose = get_playerstats_names_and_verbose()
        player_ranking = get_player_ranking(self.kwargs['year'])
        player_ranking_cleaned = prepare_player_ranking(player_ranking,
                                                        playerstats_verbose)

        context['player_ranking'] = player_ranking_cleaned.to_dict('records')

        return context
