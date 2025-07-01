# from django.core.management.base import BaseCommand, CommandError
# # from populate import initiate //give us problem bc of path situation
# from djangoapp.populate import initiate
# from .models import CarModel
from django.core.management.base import BaseCommand, CommandError
from djangoapp.populate import initiate
from djangoapp.models import CarModel


class Command(BaseCommand):
    help = 'Populates the database with initial car data(CarMake and CarModel)'

    def handle(self, *args, **options):
        try:
            if not CarModel.objects.exists():
                initiate()
                self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial car data'))
            else:
                self.stdout.write(self.style.WARNING('Database already contains car data. Skipping population.'))
        except Exception as e:
            raise CommandError(f"Failed to populate database: {e}")
