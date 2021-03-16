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
    """Create team ranking. Teams are sorted by total points"""
    model = Game
    context_object_name = 'games'

    def get_forfeit_games(self):
        """Count wins and losses (by forfeit) for each team. Return as pd df."""
        # Save all forfeit games into df
        all_games = Game.objects.filter(forfeit__isnull=False)
        df = pd.DataFrame(list(all_games.values()))

        # Add info about forfeit winner id
        df.loc[df['team_1_id'] == df['forfeit_id'], 'forfeit_winner_id'] = df['team_2_id']
        df.loc[df['team_2_id'] == df['forfeit_id'], 'forfeit_winner_id'] = df['team_1_id']

        # Count all losses and wins by forfeit
        x = df['forfeit_winner_id'].value_counts().rename_axis('team').reset_index(name='forfeit_wins')
        y = df['forfeit_id'].value_counts().rename_axis('team').reset_index(name='forfeit_losses')

        # Summary table - aggregated losses and wins for each team
        merged = y \
            .merge(x, left_on='team', right_on='team', how='outer') \
            .fillna(0)  # NaN replace to 0 forfeits

        return merged

    def check_games_result(self):
        """
        For each game check if the team lost or won. Return as pd df.
        Each row should contain team1, team2.
        Each game id should have 2 rows - 1 row for winner, and 1 row for looser.
        Each row contains points for team 1 for a certain game (2 - win, 1 - loss)
        """
        # Calculate total points, group by team and game
        stats = PS.objects \
            .values('player__team_id', 'game_id') \
            .annotate(total_points=Sum('q1_foul'))

        # Make 2 copies of stats, store as a df
        df_stats = pd.DataFrame(stats)
        df_stats2 = df_stats.copy()[
            ['player__team_id', 'game_id', 'total_points']]

        # Self join -> For each game there will be also opponent points
        merged = pd.merge(df_stats, df_stats2, on='game_id')

        # Drop rows which contain score for the same team twice
        merged = merged.query('player__team_id_x != player__team_id_y')
        merged.rename(columns={'total_points_y': 'opponent_pts'}, inplace=True)

        # Points: 2 pts for win, 1 point for loss
        merged.loc[merged['total_points_x'] > merged['opponent_pts'], 'total_pts'] = 2
        merged.loc[merged['total_points_x'] < merged['opponent_pts'], 'total_pts'] = 1

        return merged

    def calc_ranking(self, game_table, forfeits):
        """Create team ranking including wins by forfeits."""
        # Calculate total points (sum)
        total_points = game_table.groupby(['player__team_id_x'], as_index=False).sum()

        # Combine df with forfeit df
        games_result = total_points\
            .merge(forfeits, left_on='player__team_id_x', right_on='team', how='outer')
        games_result['total_pts'] = games_result['total_pts'] + games_result['forfeit_wins'] * 2

        # Ranking sorted by total points
        games_result.sort_values(by=['total_points_x'], inplace=True, ascending=False)

        return games_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        games_result = self.check_games_result()
        forfeits = self.get_forfeit_games()
        ranking = self.calc_ranking(games_result, forfeits)

        context['test'] = forfeits
        context['merge'] = ranking.to_dict('records')

        return context
