from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ArtistRating
import core.utils as utils

@receiver(post_save, sender=ArtistRating)
def artist_activity_post_save(sender, **kwargs):
    print('Entered signal')
    # utils.recalculate()