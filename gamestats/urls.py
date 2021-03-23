from django.urls import path
from . import views


app_name = 'gamestats'
template_dir = 'gamestats/'

urlpatterns = [
    path('ranking/',
         views.GameStatsList.as_view(template_name=template_dir + 'gamestats-ranking.html'),
         name='ranking'),
]
