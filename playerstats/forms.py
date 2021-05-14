from django import forms
from .models import PlayerStatistics as PS
from gamestats.models import GameStats as GS
from game.models import Game
from mysite.models import Player


class PlayerStatisticsForm(forms.ModelForm):
    """
    Display only unfinished (without all stats) games
    and players which don't have statistics related to the chosen game.
    """
    class Meta:
        model = PS
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        not_ended_games_ids = GS.get_not_ended_games_ids()
        teams_ids = GS.get_not_ended_games_teams_ids()
        unassigned_players_ids = PS.get_unassigned_players(not_ended_games_ids)
        unassigned_players = Player.objects \
            .filter(team_id__in=teams_ids) \
            .exclude(id__in=unassigned_players_ids)

        self.fields['player'].queryset = unassigned_players
        self.fields['game'].queryset = Game.objects.filter(id__in=not_ended_games_ids)

        for field in self.fields.values():
            field.label = field.help_text
            field.widget.attrs['class'] = 'form__input'
