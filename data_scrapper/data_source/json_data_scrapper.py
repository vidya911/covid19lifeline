from .scrapper_core import AbstractBaseScrapper, BaseScrapper
from core.models import City, State


class JSONScrapper(AbstractBaseURLScrapper, BaseScrapper, DataUploader):
    """
    Extract data from URL source which return data in JSON format
    """

    def __init__(self, url, state=None, service_type=None):
        self.url = url
        self.all_urls = []
        self.state = self.get_state_name(state)
        self.service_type = service_type

    def get_all_urls_from_source_urls(self):
        self.all_urls.append(url)

    def parse_data_from_source(self):
        self.response_data = []
        for url in self.all_urls:
            res = self.make_request(url)
            self.response_data.extend(res.json())
        return self.response_data

    def run(self):
        pass
