from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from .models import GameStats as GS
from playerstats.models import PlayerStatistics as PS
from helpers import flatten_dict
import pandas as pd
from game.models import Season
from game.forms import SeasonSearchForm


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

        ranking = GS.get_team_ranking(season)
        ranking.rename(columns=stats_fields_verbose_names, inplace=True)

        additional_legend = {
            'WO_win': {'verbose_name': 'W/O W', 'help_text': 'Wygrane walkowerem'},
            'WO_lost': {'verbose_name': 'W/O P', 'help_text': 'Przegrane walkowerem'},
        }

        context['ranking'] = ranking.to_dict('records')
        context['legend'] = PS.create_legend(additional_fields=additional_legend, fields_to_remove=['time'])
        context['year'] = season

        return context
