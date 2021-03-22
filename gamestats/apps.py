from django.apps import AppConfig


class GamestatsConfig(AppConfig):
    name = 'gamestats'

    def ready(self):
        import gamestats.signals
