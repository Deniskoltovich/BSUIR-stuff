from django.contrib.auth import get_user_model, authenticate

from users.abstract.services import IRegistrationService


class RegistrationService(IRegistrationService):
    @staticmethod
    def register(cleaned_data:dict):
        username = cleaned_data.get('fullname')
        password = cleaned_data.get('password')
        # cоздаем юзера, потом аутентифицируем его
        get_user_model().objects.create_user(username=username, password=password)

        user = authenticate(username=username, password=password)
        return user
