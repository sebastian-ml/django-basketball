from game.models import Game
from django.views.generic import TemplateView


class Home(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()

        return context