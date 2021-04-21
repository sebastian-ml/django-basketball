from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Game


class GameCreate(CreateView):
    model = Game
    fields = ['date', 'team_1', 'team_2', 'season']
    success_url = reverse_lazy('game:add')


class GameSchedule(ListView):
    model = Game
    context_object_name = 'games'