from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix migration history by manually inserting users.0001_initial'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if migration already exists
            cursor.execute("""
                SELECT COUNT(*) FROM django_migrations 
                WHERE app = 'users' AND name = '0001_initial'
            """)
            exists = cursor.fetchone()[0]
            
            if not exists:
                # Insert the migration record
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('users', '0001_initial', NOW())
                """)
                self.stdout.write(
                    self.style.SUCCESS('Successfully inserted users.0001_initial migration record')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Migration users.0001_initial already exists')
                )
