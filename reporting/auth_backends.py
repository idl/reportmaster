from django.contrib.auth.backends import ModelBackend
from .models import IDLUser
#from django.contrib.auth.models import User

class IDLUserBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return IDLUser.objects.get(pk=user_id)
        except IDLUser.DoesNotExist:
            return None