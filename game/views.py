from .models import Game
from mysite.models import PlayerStatistics as PS
from django.urls import reverse_lazy
from django.db.models import Sum
import pandas as pd
from django.views.generic import CreateView, ListView


class GameCreate(CreateView):
    model = Game
    fields = ['date', 'team_1', 'team_2', 'season']
    success_url = reverse_lazy('game:game-add')


class GameRankingList(ListView):
    model = Game
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total points, group by team and game
        stats = PS.objects \
            .values('player__team_id', 'game_id') \
            .annotate(total_points=Sum('q1_foul'))

        context['aggr_player_stats'] = stats  # delete this

        # Make 2 copies of stats, store as a df
        df_stats = pd.DataFrame(stats)
        df_stats2 = df_stats.copy()[['player__team_id', 'game_id', 'total_points']]

        # Self join -> For each game there will be also opponent points
        merged = pd.merge(df_stats, df_stats2, on='game_id')

        # Drop rows which contain score for the same team twice
        merged = merged.query('player__team_id_x != player__team_id_y')

        merged.rename(columns={'total_points_y': 'opponent_pts'}, inplace=True)

        # Points: 2 pts for win, 1 point for loss
        merged.loc[merged['total_points_x'] > merged['opponent_pts'], 'result'] = 2
        merged.loc[merged['total_points_x'] < merged['opponent_pts'], 'result'] = 1

        # Calculate total points and sort
        merged = merged.groupby(['player__team_id_x'], as_index=False).sum()
        merged.sort_values(by=['total_points_x'], inplace=True, ascending=False)

        context['merge'] = merged.to_dict('records')

        return context
