from django.core.management.base import BaseCommand, CommandError
from core.models import UserProfile, ArtistRating
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads users artists ratings from csv'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs=1, type=str)
    
    def handle(self, *args, **options):
        file_path = options['file_path'][0]

        with open(file_path) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:

                self.stdout.write('Row: "%s"' % row)

                user_id = row[1]
                user = UserProfile.objects.get(id=user_id)

                artist_rating, created = ArtistRating.objects.get_or_create(
                    user_profile=user,
                    artist_name=row[2],
                    rating=row[3]
                )

                if created:
                    self.stdout.write(self.style.SUCCESS('Created artist rating: "%s"' % artist_rating.artist_name))
                else:
                    self.stdout.write(self.style.WARNING('Artist rating "%s" already exists' % artist_rating.artist_name))
            