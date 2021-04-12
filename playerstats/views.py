from .models import PlayerStatistics
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
import pandas as pd


class PlayerStatsCreate(CreateView):
    """Add player statistics which belongs to certain game."""
    model = PlayerStatistics
    fields = '__all__'
    success_url = reverse_lazy('home:player-stats-add')


def get_player_ranking(year=None):
    """Get aggregated player stats."""
    player_stats = PlayerStatistics.objects.all()

    if year:
        player_stats = PlayerStatistics.objects.filter(game__season__year=year)

    # Get field names and extend by needed additional fields
    field_names = list(player_stats.values()[0].keys())
    field_names.extend(('player__first_name', 'player__last_name', 'player__team'))

    # Calculate aggr stats for each player
    df = pd.DataFrame(list(player_stats.values(*field_names)))
    stats = df.groupby(['player_id', 'player__first_name', 'player__last_name', 'player__team'], as_index=False).sum()

    return stats.to_dict('records')


class PlayerStatsList(ListView):
    """Show player stats ranking list."""
    model = PlayerStatistics

    # Note: Currently it contains only fouls - will be expanded in the future
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_ranking'] = get_player_ranking()

        return context


class PlayerStatsSeasonList(ListView):
    """Show player stats ranking list for a specific season."""
    model = PlayerStatistics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_ranking'] = get_player_ranking(self.kwargs['year'])

        return context
