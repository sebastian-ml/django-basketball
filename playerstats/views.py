from django.views.generic.edit import FormMixin
from game.models import Season
from game.forms import SeasonSearchForm
from helpers import flatten_dict
from .models import PlayerStatistics as PS
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import PlayerStatisticsForm


class PlayerStatsCreate(CreateView):
    """Create player statistics which belongs to the certain game."""
    form_class = PlayerStatisticsForm
    success_url = reverse_lazy('playerstats:add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seasons'] = SeasonSearchForm

        return context


class PlayerStatsList(ListView):
    model = PS
    context_object_name = 'playerstats'
    paginate_by = 10
    ordering = ['-game__date', 'player__team__name', 'player__last_name']


class PlayerStatsRanking(FormMixin, ListView):
    """Show player stats ranking list."""
    model = PS
    form_class = SeasonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats_fields_meta = PS.get_stats_fields_meta()
        stats_fields_verbose_names = flatten_dict(stats_fields_meta,
                                                  'verbose_name')

        # Create general player ranking or for selected season
        season = self.request.GET.get('season', None)

        player_ranking = PS.get_clean_player_ranking(stats_fields_verbose_names, season)
        legend = PS.create_legend()

        context['player_ranking'] = player_ranking.to_dict('records')
        context['legend'] = legend
        context['year'] = season

        return context
