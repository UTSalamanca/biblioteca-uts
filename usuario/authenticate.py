from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomBackend():
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(login=username)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, cve_persona):
        try:
            return User.objects.get(pk=cve_persona)
        except:
            return None
