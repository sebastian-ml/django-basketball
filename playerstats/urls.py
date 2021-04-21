from django.urls import path
from . import views


app_name = 'playerstats'
template_dir = 'playerstats/'

urlpatterns = [
    path('statistics/add/',
         views.PlayerStatsCreate.as_view(
             template_name=template_dir + 'add.html'
         ),
         name='add'),
    path('ranking/',
         views.PlayerStatsRanking.as_view(
             template_name=template_dir + 'ranking.html'
         ),
         name='ranking'),
    path('ranking/season=<int:year>/',
         views.PlayerStatsRanking.as_view(
             template_name=template_dir + 'ranking.html'
         ),
         name='ranking-by-season'),
]