from django.db.models.signals import post_save, pre_save
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


@receiver(pre_save, sender=Game)
def update_game_stats(sender, instance, **kwargs):
    before_save = Game.objects.get(id=instance.id)

    if before_save.team_2 != instance.team_2:
        GameStats.objects \
            .filter(game=instance, team=before_save.team_2) \
            .update(team=instance.team_2)

    if before_save.team_1 != instance.team_1:
        GameStats.objects \
            .filter(game=instance, team=before_save.team_1) \
            .update(team=instance.team_1)
