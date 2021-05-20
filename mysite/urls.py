from django.urls import path
from . import views

app_name = 'home'
template_dir = 'mysite/'

urlpatterns = [
    path('',
         views.Home.as_view(template_name=template_dir + 'home.html'),
         name='home'),
    path('teams/',
         views.TeamsList.as_view(template_name=template_dir + 'teams.html'),
         name='teams-list'),
    path('teams/<str:pk>/',
         views.TeamDetail.as_view(template_name=template_dir + 'team.html'),
         name='team-profile'),
    path('players/',
         views.PlayerList.as_view(template_name=template_dir + 'players.html'),
         name='players-list'),
    path('players/<int:pk>/',
         views.PlayerDetail.as_view(template_name=template_dir + 'player.html'),
         name='player-profile'),
]
