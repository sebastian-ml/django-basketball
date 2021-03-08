from .models import PlayerStatistics
from django.urls import reverse_lazy
from django.views.generic import CreateView


class PlayerStatsCreate(CreateView):
    model = PlayerStatistics
    fields = '__all__'
    success_url = reverse_lazy('home:player-stats-add')
