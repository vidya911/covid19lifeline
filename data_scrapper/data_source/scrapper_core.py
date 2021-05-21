import abc
from django.core.exceptions import ObjectDoesNotExist
from retrying import retry
import requests

from hospital.models import Hospital
from core.models import City, State


def retry_if_connection_error(exception):
    return isinstance(exception, ConnectionError)


class AbstractBaseURLScrapper(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def get_all_urls_from_source_urls(self):
        pass


    @abc.abstractmethod
    def parse_data_from_source(self):
        pass


    @abc.abstractmethod
    def run(self):
        pass


class BaseScrapper(object):


    @staticmethod
    @retry(retry_on_exception=retry_if_connection_error, wait_fixed=2000)
    def make_request(url):
        res = requests.get(url)
        return res


    @staticmethod
    def get_state_name(state_name):
        try:
            _state = State.objects.get(name=state_name)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("State: %s does not exist", state_name)
        return _state.name

