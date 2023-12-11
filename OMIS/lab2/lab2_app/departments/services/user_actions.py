from http.client import HTTPResponse

from users.models import Activity

from departments.abstract.services import IUserActionsService


class EnterError(Exception):
    pass


class ExitError(Exception):
    pass


class UserActionsService(IUserActionsService):
    @staticmethod
    def do_enter(user, department):
        user_activity = Activity.objects.filter(user=user).first()
        if user_activity and user_activity.action == 'enter':
            raise EnterError
        UserActionsService.save_action(department, user, 'enter')


    @staticmethod
    def do_exit(user):
        user_activity = Activity.objects.filter(user=user).first()
        if not user_activity or user_activity.action == 'exit':
            raise ExitError

        UserActionsService.save_action(user_activity.department, user, 'exit')

    @staticmethod
    def save_action(department, user, action:str):
        Activity.objects.create(department=department, user=user, action=action)
