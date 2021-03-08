from .models import Game
from django.urls import reverse_lazy
from django.views.generic import CreateView


class GameCreate(CreateView):
    model = Game
    fields = ['date', 'team_1', 'team_2', 'season']
    success_url = reverse_lazy('game:game-add')
