from django.views.generic.edit import FormMixin
# from game.forms import SeasonSearchForm
from helpers import flatten_dict, get_stats_fields_meta
from .models import PlayerStatistics as PS
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import PlayerStatisticsForm


def clear_player_ranking(ranking, colnames):
    """Rename colnames and delete unnecesary columns.

    Keyword arguments:
    ranking -- player ranking (as pandas df)
    colnames -- dictionary with old and new colnames. Must be in the following format:
    {"col1_old_name": "col1_new_name", "col2_old_name": "col2_new_name"}
    """

    all_cols = {**colnames,
                'player__first_name': 'Imię', 'player__last_name': 'Nazwisko',
                'player__team': 'Drużyna', 'time': 'T', 'player_id': '#',
                'game_counter': 'Mecze'}

    ranking.rename(columns=all_cols, inplace=True)
    ranking.drop(columns=['game_id', 'id'], inplace=True)

    return ranking


class PlayerStatsCreate(CreateView):
    """Create player statistics which belongs to the certain game."""
    form_class = PlayerStatisticsForm
    success_url = reverse_lazy('playerstats:add')


class PlayerStatsRanking(FormMixin, ListView):
    """Show player stats ranking list."""
    model = PS
    # form_class = SeasonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats_fields_meta = get_stats_fields_meta(PS)
        stats_fields_verbose_names = flatten_dict(stats_fields_meta,
                                                  'verbose_name')

        # Create general player ranking or for some season
        season = self.request.GET.get('season', None)
        player_ranking = PS.get_player_ranking(season)
        player_ranking_cleaned = clear_player_ranking(player_ranking,
                                                      stats_fields_verbose_names)

        context['player_ranking'] = player_ranking_cleaned.to_dict('records')
        context['legend'] = stats_fields_meta
        context['year'] = season

        return context
