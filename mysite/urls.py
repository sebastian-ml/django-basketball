from django.urls import path
from . import views


app_name = 'home'
template_dir = 'mysite/'

urlpatterns = [
    path('player/statistics/add/',
         views.PlayerStatsCreate.as_view(
             template_name=template_dir + 'player-statistics-add.html'
         ),
         name='player-stats-add'),
    path('player/ranking/',
         views.PlayerStatsList.as_view(
             template_name=template_dir + 'player-ranking.html'
         ),
         name='player-ranking'),
    path('player/ranking/season=<int:year>/',
         views.PlayerStatsSeasonList.as_view(
             template_name=template_dir + 'player-ranking.html'
         ),
         name='player-ranking-by-season'),
]