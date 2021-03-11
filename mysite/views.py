from .models import PlayerStatistics
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import CreateView, ListView


class PlayerStatsCreate(CreateView):
    """Add player statistics which belongs to certain game."""
    model = PlayerStatistics
    fields = '__all__'
    success_url = reverse_lazy('home:player-stats-add')


class PlayerStatsList(ListView):
    model = PlayerStatistics
    context_object_name = 'player_stats'

    # Note: Currently it contains only fouls - will be expanded in the future
    def get_context_data(self, **kwargs):
        """Perform statistics aggregation for each player from all games."""
        context = super().get_context_data(**kwargs)

        context['player_rank'] = PlayerStatistics.objects\
            .values('player__id')\
            .annotate(total_fouls=Sum('q1_foul'))\
            .order_by('-total_fouls')

        return context
