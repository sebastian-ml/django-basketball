from .models import Player
from game.models import Team
from gamestats.models import GameStats as GS
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView
)


class Home(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = GS \
            .get_game_schedule_with_score() \
            .to_dict('records')

        return context


class TeamsList(ListView):
    model = Team
    context_object_name = 'teams'


class PlayerDetail(DetailView):
    model = Player
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player = self.get_object()
        context['full_name'] = player.get_full_name()

        return context


class PlayerList(ListView):
    model = Player
    context_object_name = 'players'
