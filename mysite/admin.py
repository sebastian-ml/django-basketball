from django.contrib import admin
from .models import Team, Player, PlayerStatistics


# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayerStatistics)
