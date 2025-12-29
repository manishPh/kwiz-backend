from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Reset admin user password and ensure superuser permissions'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to reset')
        parser.add_argument('password', type=str, help='New password')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'Found user: {username}')
            self.stdout.write(f'  Email: {user.email}')
            self.stdout.write(f'  Is staff: {user.is_staff}')
            self.stdout.write(f'  Is superuser: {user.is_superuser}')
            self.stdout.write(f'  Is active: {user.is_active}')
            
            # Update password and permissions
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully reset password and permissions for {username}'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            self.stdout.write('Available users:')
            for u in User.objects.all():
                self.stdout.write(f'  - {u.username} (staff={u.is_staff}, super={u.is_superuser})')

