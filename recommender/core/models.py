from django.db import models


class UserProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'm'
        FEMALE = 'f'

    id = models.CharField('User ID', max_length=50, primary_key=True)
    gender = models.CharField('Gender', max_length=1, null=True, blank=True, choices=Gender.choices)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField('Country', max_length=50, null=True, blank=True)
    registered_at = models.DateField()


class SongActivity(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='song_activities')
    artist_name = models.CharField('Artist name', max_length=100)
    track_name = models.CharField('Track name', max_length=150)
    timestamp = models.DateTimeField()


class ArtistRating(models.Model):

    class SimilarityTechnique(models.TextChoices):
        JACCARD = 'Jaccard'
        COSENO = 'Coseno'
        PEARSON = 'Pearson'

    class RecommenderModelType(models.TextChoices):
        USER_USER = 'User user'
        ITEM_ITEM = 'Item item'

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='artist_ratings')
    artist_name = models.CharField('Artist name', max_length=100)
    activity_count = models.IntegerField('Activity count')
    ratings = models.FloatField()
    similarity_technique = models.CharField(choices=SimilarityTechnique.choices)
    model_type = models.CharField(choices=RecommenderModelType.choices)


class Neighbour(models.Model):
    artist_rating = models.ForeignKey('ArtistRating', on_delete=models.CASCADE, related_name='neighbours')
    name = models.CharField('Name', max_length=100)
