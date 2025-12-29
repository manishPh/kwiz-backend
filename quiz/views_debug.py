from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()

@csrf_exempt
def debug_login(request):
    """Debug endpoint to test authentication"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Try to get user
            try:
                user = User.objects.get(username=username)
                user_exists = True
                is_staff = user.is_staff
                is_superuser = user.is_superuser
                is_active = user.is_active
                password_correct = user.check_password(password)
            except User.DoesNotExist:
                user_exists = False
                is_staff = False
                is_superuser = False
                is_active = False
                password_correct = False
            
            # Try authentication
            auth_user = authenticate(username=username, password=password)
            auth_success = auth_user is not None
            
            return JsonResponse({
                'user_exists': user_exists,
                'is_staff': is_staff,
                'is_superuser': is_superuser,
                'is_active': is_active,
                'password_correct': password_correct,
                'auth_success': auth_success,
                'all_users': list(User.objects.values_list('username', flat=True))
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'message': 'POST username and password to test'})

