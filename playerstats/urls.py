from django.urls import path
from . import views


app_name = 'playerstats'
template_dir = 'player-stats/'

urlpatterns = [
    path('statistics/add/',
         views.PlayerStatsCreate.as_view(
             template_name=template_dir + 'player-statistics-add.html'
         ),
         name='player-stats-add'),
    path('ranking/',
         views.PlayerStatsRanking.as_view(
             template_name=template_dir + 'player-ranking.html'
         ),
         name='player-ranking'),
    path('ranking/season=<int:year>/',
         views.PlayerStatsRanking.as_view(
             template_name=template_dir + 'player-ranking.html'
         ),
         name='player-ranking-by-season'),
]