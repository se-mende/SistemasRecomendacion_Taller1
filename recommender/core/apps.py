from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # importing model classes
        # from .models import ArtistRating  # or...
        # artist_rating = self.get_model('ArtistRating')
        import core.signals

        # registering signals with the model's string label
        # post_save.connect(receiver, sender='core.ArtistRating')
