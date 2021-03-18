from django.urls import path
from . import views


app_name = 'game'
template_dir = 'game/'

urlpatterns = [
    path('add/',
         views.GameCreate.as_view(template_name=template_dir + 'game-add.html'),
         name='game-add'),
    path('ranking/',
         views.GameRankingList.as_view(template_name=template_dir + 'game-ranking.html'),
         name='game-ranking'),
]
