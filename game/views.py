from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Game


class GameCreate(CreateView):
    model = Game
    fields = ['date', 'team_1', 'team_2', 'season']
    success_url = reverse_lazy('game:game-add')
