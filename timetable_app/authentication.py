# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# class IdentificationNumberBackend(ModelBackend):
#     """
#     Custom authentication backend to authenticate users using their identification number.
#     """
#     def authenticate(self, request, identification_number=None, password=None, **kwargs):
#         User = get_user_model()
#         try:
#             user = User.objects.get(identification_number=identification_number)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class IdentificationNumberBackend(ModelBackend):
    """
    Custom authentication backend to authenticate users using their identification number.
    """
    def authenticate(self, request, identification_number=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(identification_number=identification_number)
            if user.check_password(password):
                user.backend = 'timetable_app.authentication.IdentificationNumberBackend'  # Add this line
                return user
        except User.DoesNotExist:
            return None
