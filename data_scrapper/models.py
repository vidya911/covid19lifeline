from django.db import models
from django.conf import settings


from core.models import City, State, NameBaseConfig, BasicConfiguration, ServiceType

SCRAPPER_RUN_STATUS = (
                      ('RUNNING', 'RUNNING'),
                      ('SUCCESS', 'SUCCESS'),
                      ('FAILED', 'FAILED')
)


def scrapped_data_upload_path():
    #TODO: change to upload path
    return '/tmp'

class ScrapperByURL(NameBaseConfig):
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    service_type = models.ForeignKey(ServiceType, on_delete=models.DO_NOTHING)
    source_url = models.URLField(blank=True, null=True)
    scraper_module = models.CharField(max_length=255)


### ToDo implement data source model by twitter and google


class ScrapperByURLRunLog(BasicConfiguration):
    data_source = models.ForeignKey(ScrapperByURL, on_delete=models.DO_NOTHING)
    run_status = models.CharField(choices=SCRAPPER_RUN_STATUS, max_length=10)
    error_log = models.TextField(blank=True, null=True)
    success_log = models.TextField(blank=True, null=True)
    data_csv_data = models.FileField(upload_to=scrapped_data_upload_path)
