from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path(
        'add',
        views.GameCreate.as_view(template_name='game/game-add.html'),
        name='game-add'
    ),
]