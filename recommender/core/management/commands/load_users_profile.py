from django.core.management.base import BaseCommand, CommandError
from core.models import UserProfile
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads users csv'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs=1, type=str)
    
    def handle(self, *args, **options):
        file_path = options['file_path'][0]

        with open(file_path) as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)
            for row in reader:

                self.stdout.write(self.style.NOTICE('Row: "%s"' % row))

                user, created = UserProfile.objects.get_or_create(
                    id=row[0],
                    gender=row[2] if row[2] != '' else None,
                    age=row[2] if row[2] != '' else None,
                    country=row[3],
                    registered_at=datetime.strptime(row[4], '%b %d, %Y') if row[4] != '' else None 
                )

                if created:
                    self.stdout.write(self.style.SUCCESS('Created user: "%s"' % user.id))
                else:
                    self.stdout.write(self.style.WARNING('User "%s" already exists' % user.id))