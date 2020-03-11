from django.db import models


class UserProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'm'
        FEMALE = 'f'

    id = models.CharField('User ID', max_length=50, primary_key=True)
    gender = models.CharField('Gender', max_length=1, null=True, blank=True, choices=Gender.choices)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField('Country', max_length=50, null=True, blank=True)
    registered_at = models.DateField(null=True)

    def __str__(self):
        return self.id


class SongActivity(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='song_activities')
    artist_name = models.CharField('Artist name', max_length=100)
    track_name = models.CharField('Track name', max_length=150)
    timestamp = models.DateTimeField()


class ArtistActivity(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='artists_activities')
    artist_name = models.CharField('Artist name', max_length=120)
    activity_count = models.PositiveIntegerField()
    
    def __str__(self):
        return 'User: %s | Artist name: %s' % (self.user_profile.pk, self.artist_name)


class ArtistRating(models.Model):

    class SimilarityTechnique(models.TextChoices):
        JACCARD = 'jaccard'
        COSINE = 'cosine'
        PEARSON = 'pearson'

    class RecommenderModelType(models.TextChoices):
        USER_USER = 'User user'
        ITEM_ITEM = 'Item item'

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='artist_ratings')
    artist_name = models.CharField('Artist name', max_length=100)
    # activity_count = models.IntegerField('Activity count')
    rating = models.FloatField()
    # similarity_technique = models.CharField(max_length=50, choices=SimilarityTechnique.choices)
    # model_type = models.CharField(max_length=50, choices=RecommenderModelType.choices)

    def __str__(self):
        return 'User: "%s" | Artist name: "%s" | Rating "%f"' % (self.user_profile.pk, self.artist_name, self.rating)


class Neighbour(models.Model):
    artist_rating = models.ForeignKey('ArtistRating', on_delete=models.CASCADE, related_name='neighbours')
    name = models.CharField('Name', max_length=100)
