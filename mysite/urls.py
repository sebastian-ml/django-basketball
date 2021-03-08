from django.urls import path
from . import views


app_name = 'home'
template_dir = 'mysite/'

urlpatterns = [
    path(
        'player/statistics/add',
        views.PlayerStatsCreate.as_view(
            template_name=template_dir + 'player-statistics-add.html'
        ),
        name='player-stats-add'
    ),
]