from django.db.models.signals import post_save
from .models import GameStats
from game.models import Game
from django.dispatch import receiver


@receiver(post_save, sender=Game)
def create_game_stats(sender, instance, created, **kwargs):
    """
    For each game create 2 instances of GameStats.
    One instance per one team.
    """
    if created:
        GameStats.objects.create(game=instance, team=instance.team_1)
        GameStats.objects.create(game=instance, team=instance.team_2)
