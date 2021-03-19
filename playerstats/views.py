from .models import PlayerStatistics
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.views.generic import CreateView, ListView


class PlayerStatsCreate(CreateView):
    """Add player statistics which belongs to certain game."""
    model = PlayerStatistics
    fields = '__all__'
    success_url = reverse_lazy('home:player-stats-add')


def get_player_ranking(year=None):
    """Get player stats from all seasons or from a certain season."""
    player_stats = PlayerStatistics.objects.all()
    if year:
        player_stats = PlayerStatistics.objects.filter(game__season__year=year)

    return player_stats.values('player__id') \
        .annotate(total_fouls=Sum('q1_foul'),
                  games_played=Count('q1_foul')) \
        .order_by('-total_fouls')


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
