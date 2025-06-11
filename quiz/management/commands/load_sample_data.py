from django.core.management.base import BaseCommand
from quiz.sample_data import create_sample_data


class Command(BaseCommand):
    help = 'Load sample Bollywood quiz data'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        create_sample_data()
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
