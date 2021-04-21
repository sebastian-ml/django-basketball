from django.urls import path
from . import views


app_name = 'gamestats'
template_dir = 'gamestats/'

urlpatterns = [
    path('ranking/',
         views.GameStatsList.as_view(
             template_name=template_dir + 'ranking.html'
         ),
         name='ranking'),
    path('ranking/season=<int:year>/',
         views.GameStatsList.as_view(
             template_name=template_dir + 'ranking.html'
         ),
         name='ranking-by-season'),
]
