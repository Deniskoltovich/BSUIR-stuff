from abc import ABC, abstractmethod


class IUserManagementService(ABC):
    @staticmethod
    @abstractmethod
    def get_employees():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_user_activities(user_id: int):
        raise NotImplementedError


class IRegistrationService(ABC):
    @staticmethod
    @abstractmethod
    def register(cleaned_data: dict):
        raise NotImplementedError


class IEmployeeProfileService(ABC):
    @staticmethod
    @abstractmethod
    def create_profile(cleaned_data: dict):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def save_profile(username: str, password: str):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def change_password(user, new_password: str):
        raise NotImplementedError


class IAccessChangingService(ABC):
    @staticmethod
    @abstractmethod
    def remove_employee_access(employee, department):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def remove_group_access(user_group, department):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def add_employee_access(employee, department):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def add_group_access(user_group, department):
        raise NotImplementedError
