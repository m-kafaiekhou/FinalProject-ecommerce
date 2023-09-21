from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PhoneNumberModelBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        user_model = get_user_model()

        if phone_number is None:
            return None

        users = user_model.objects.filter(phone_number=phone_number)

        # Test whether any matched user has the provided password:
        for user in users:
            if user.check_password(password):
                return user
        if not users:
            user_model().set_password(password)
