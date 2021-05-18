from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=40, primary_key=True)

    class Meta:
        db_table = 'team'

    def __str__(self):
        return f'{self.name}'


class Player(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'player'

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}' \
               f' ({self.team.name})'
