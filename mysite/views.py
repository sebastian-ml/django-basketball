from game.models import Team
from django.views.generic import TemplateView, ListView
from gamestats.models import GameStats as GS


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
