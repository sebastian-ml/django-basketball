from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.views.generic import CreateView, ListView
from .models import Game
from playerstats.models import PlayerStatistics as PS
import pandas as pd


def get_valid_games_ids(num_of_stats):
    """Return queryset with games ids which have assigned 4 player stats."""
    total_assigned_stats = PS.objects.all() \
        .values('game') \
        .annotate(total=Count('game'))
    games_with_full_stats = total_assigned_stats.filter(total=num_of_stats)
    valid_games_ids = games_with_full_stats.values_list('game', flat=True)

    return valid_games_ids


def get_forfeit_games():
    """Count wins and losses (by forfeit) for each team. Return as pd df."""
    # Save all forfeit games into df
    all_games = Game.objects.filter(forfeit__isnull=False)
    df = pd.DataFrame(list(all_games.values()))

    # Add info about forfeit winner id
    df.loc[df['team_1_id'] == df['forfeit_id'], 'forfeit_winner_id'] = df['team_2_id']
    df.loc[df['team_2_id'] == df['forfeit_id'], 'forfeit_winner_id'] = df['team_1_id']

    # Count all losses and wins by forfeit
    forfeit_wins = df['forfeit_winner_id'].value_counts().rename_axis('team').reset_index(name='forfeit_wins')
    forfeit_losses = df['forfeit_id'].value_counts().rename_axis('team').reset_index(name='forfeit_losses')

    # Summary table - aggregated losses and wins for each team
    merged = forfeit_losses \
        .merge(forfeit_wins, left_on='team', right_on='team', how='outer') \
        .fillna(0)  # NaN replace to 0 forfeits

    return merged


def get_games_result(stats):
    """
    For each game check if the team lost or won. Return as pd df.
    Each row should contain team1, team2.
    Each game id should have 2 rows - 1 row for winner, and 1 row for looser.
    Each row contains points for team 1 for a certain game (2 - win, 1 - loss)
    """
    # Calculate total points, group by team and game
    aggr_game_stats = stats \
        .values('player__team_id', 'game_id') \
        .annotate(total_points=Sum('q1_foul'))

    # Make additional copy of stats, store as df
    df_stats = pd.DataFrame(aggr_game_stats)
    df_stats2 = df_stats.copy()[
        ['player__team_id', 'game_id', 'total_points']]

    # Self join -> For each game there will be also opponent points
    merged = pd.merge(df_stats, df_stats2, on='game_id')

    # Drop rows which contain score for the same team twice
    merged = merged.query('player__team_id_x != player__team_id_y')
    merged.rename(columns={'total_points_y': 'opponent_pts'}, inplace=True)

    # Points: 2 pts for win, 1 point for loss
    merged.loc[merged['total_points_x'] > merged['opponent_pts'], 'points'] = 2
    merged.loc[merged['total_points_x'] < merged['opponent_pts'], 'points'] = 1

    return merged


def calc_ranking(game_table, forfeits):
    """Create team ranking including wins by forfeits."""
    # Calculate total points (sum)
    total_points = game_table.groupby(['player__team_id_x'], as_index=False).sum()

    # Combine df with forfeit df
    games_result = forfeits \
        .merge(total_points, left_on='team', right_on='player__team_id_x', how='outer')

    # Create col with total points ('normal' + forfeit wins)
    games_result['total_pts'] = games_result['points'].fillna(0) + games_result['forfeit_wins'] * 2

    # Ranking, sorted by total points
    games_result.sort_values(by=['total_pts'], inplace=True, ascending=False)

    return games_result


class GameCreate(CreateView):
    model = Game
    fields = ['date', 'team_1', 'team_2', 'season']
    success_url = reverse_lazy('game:game-add')


class GameRankingList(ListView):
    """Create team ranking. Teams are sorted by total points"""
    model = Game
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get stats which occurs only 4 times per game id (2 teams * 2 players)
        valid_games = get_valid_games_ids(4)
        stats = PS.objects.filter(game__in=valid_games)

        # Calculate valid games results and get all wins & losses by forfeit
        games_result = get_games_result(stats)
        forfeits = get_forfeit_games()

        ranking = calc_ranking(games_result, forfeits)  # Team ranking

        context['test'] = games_result.to_dict('records')
        context['merge'] = ranking.to_dict('records')

        return context
