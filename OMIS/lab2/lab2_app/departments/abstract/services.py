from abc import ABC, abstractmethod


class IUserActionsService(ABC):
    @staticmethod
    @abstractmethod
    def do_enter(self, user, department):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def do_exit(self, user):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def save_action(self, department, user, action):
        raise NotImplementedError
