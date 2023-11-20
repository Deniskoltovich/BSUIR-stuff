from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.sessions.models import Session
from authentication.models import User



class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(
            lambda: self.__class__.get_user(request)
        )
        setattr(request, '_dont_enforce_csrf_checks', True)

    @staticmethod
    def get_user(request):
        try:
            session_id = request.session.session_key
            session = Session.objects.get(session_key=session_id)

            # Access the user ID stored in the session
            user_id = session.get_decoded().get('_auth_user_id')

            # Retrieve the user object
            user = User.objects.get(pk=user_id)

            print('user!!!', user)
            return user

        except (Session.DoesNotExist, User.DoesNotExist):
            return None
