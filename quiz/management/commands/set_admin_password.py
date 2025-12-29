from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Set password for admin user'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Delete all existing users and create fresh admin
        self.stdout.write("Deleting all existing users...")
        User.objects.all().delete()
        
        # Create fresh admin user
        username = 'admin'
        password = 'admin123'
        email = 'admin@kwiz.fun'
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created fresh admin user'))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Email: {email}')
        
        # Verify
        if user.check_password(password):
            self.stdout.write(self.style.SUCCESS('✓ Password verification: PASSED'))
        else:
            self.stdout.write(self.style.ERROR('✗ Password verification: FAILED'))

