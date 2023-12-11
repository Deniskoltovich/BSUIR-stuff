from abc import ABC, abstractmethod


class IRequestManagementService(ABC):
    @staticmethod
    @abstractmethod
    def get_requests():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_request(cleaned_data: dict, user):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def change_request_status(request_id, status):
        raise NotImplementedError
