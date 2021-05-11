from game.models import Game, Team
from django.views.generic import TemplateView, ListView


class Home(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()

        return context


class TeamsList(ListView):
    model = Team
    context_object_name = 'teams'
