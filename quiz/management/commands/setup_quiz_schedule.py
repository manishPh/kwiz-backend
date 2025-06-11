from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, time
from quiz.models import DailyQuiz


class Command(BaseCommand):
    help = 'Set up quiz release schedule for upcoming days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to set up (default: 7)',
        )
        parser.add_argument(
            '--release-time',
            type=str,
            default='00:00',
            help='Release time in HH:MM format (default: 00:00)',
        )

    def handle(self, *args, **options):
        days = options['days']
        release_time_str = options['release_time']
        
        try:
            # Parse release time
            hour, minute = map(int, release_time_str.split(':'))
            release_time = time(hour, minute)
        except ValueError:
            self.stdout.write(
                self.style.ERROR('Invalid time format. Use HH:MM (e.g., 00:00)')
            )
            return
        
        today = date.today()
        updated_count = 0
        
        self.stdout.write(f'Setting up quiz schedule for next {days} days...')
        self.stdout.write(f'Release time: {release_time_str} IST')
        
        for i in range(days):
            quiz_date = today + timedelta(days=i)
            
            # Update existing quizzes or create placeholders
            quizzes = DailyQuiz.objects.filter(date=quiz_date)
            
            if quizzes.exists():
                # Update existing quizzes
                for quiz in quizzes:
                    quiz.release_time = release_time
                    quiz.save()
                    updated_count += 1
                    self.stdout.write(f'  ✓ Updated {quiz_date}: {quiz.title}')
            else:
                # Create placeholder for future quiz
                self.stdout.write(f'  ⚠ No quiz found for {quiz_date} - create one using quiz configs')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} quizzes')
        )
        self.stdout.write(
            self.style.WARNING('Remember to create quiz configs for missing dates!')
        )
