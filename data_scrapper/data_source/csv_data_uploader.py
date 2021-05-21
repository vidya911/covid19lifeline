import os
import csv
import datetime
import json


from .scrapper_core import BaseScrapper
from core.models import City, State
from django.conf import settings
from core.exceptions import InvalidServiceType, InValidScrappedData
from hospital.serializers import HospitalJSONSerializer
from hospital.models import Hospital

DATA_DIR = os.path.join(settings.MEDIA_ROOT, "uploads/data_source")


class DataUploader(BaseScrapper):

    SERVICE_TYPE = ['hospital']

    SERIALIZER_MAPPING = {
            'hospital': HospitalJSONSerializer
    }

    MODEL_MAPPING = {
            'hospital': Hospital
    }


    MANDATORY_FIELD_MAPPING = {
            'hospital': ['name', 'state', 'city'],
    }


    def __init__(self, json_data, service_type):
        self.json_data = DataUploader.clean_json_data(json_data)
        self.service_type = service_type
        self.validate_init_data(self.json_data, self.service_type)


    def validate_init_data(self, json_data, service_type):
        if self.service_type not in DataUploader.SERVICE_TYPE:
            raise InvalidServiceType("Invalid service type: %s", self.service_type)
        mandatory_fields = DataUploader.MANDATORY_FIELD_MAPPING.get(self.service_type)
        for each in json_data:
            for field in mandatory_fields:
                try:
                    field_val = each[field]
                except KeyError:
                    raise InValidScrappedData("JSON data doesn't contain data for mandatory field: %s", field)
        return True

    @classmethod
    def clean_json_data(cls, json_data):
        _json_data = [{k:v for k, v in each.items() if v != ''} for each in json_data]
        return _json_data

    @classmethod
    def upload_from_csv_file(cls, file_path, service_type):
        json_data = []
        with open(file_path, encoding='utf-8') as csvb:
            csv_reader = csv.DictReader(csvb)
            for row in csv_reader:
                json_data.append(row)
        return cls(json_data, service_type)


    @classmethod
    def upload_from_json_file(cls, file_path, service_type):
        with open(file_path, 'r') as fj:
            json_data = json.load(fj)
        return cls(json_data, service_type)


    @classmethod
    def get_serializer_class(cls, service_type):
        try:
            serializer_class = cls.SERIALIZER_MAPPING[service_type]
        except KeyError:
            raise
        return serializer_class

    @classmethod
    def get_model_class(cls, service_type):
        try:
            model_class = cls.MODEL_MAPPING[service_type]
        except KeyError:
            raise
        return model_class

    def validate_each_data(self, serializer_class, data):
        serializerd_data = serializer_class(data=data)
        data['validation_error'] = ''
        if not serializerd_data.is_valid():
            data['validation_error'] = serializerd_data.errors
        return data


    def validate(self):
        try:
            serializer_class = DataUploader.get_serializer_class(self.service_type)
        except KeyError:
            raise InvalidServiceType("Scraping implementation for service type: %s is missing", service_type)
        self.validation_data_result = []
        for data in self.json_data:
            validated_data = self.validate_each_data(serializer_class, data)
            self.validation_data_result.append(validated_data)

    def get_csv_path(self):
        _time_now = datetime.datetime.now().strftime('%d-%m-%y-%H-%m-%s')
        data_dir = os.path.join(DATA_DIR, self.service_type)
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, _time_now + '.csv')
        return csv_path

    def create_result_csv(self):
        _csv_path = self.get_csv_path()
        import pdb;pdb.set_trace()
        with open(_csv_path, 'w+') as csv_file:
            dw = csv.DictWriter(csv_file, self.save_data_result[0].keys())
            dw.writeheader()
            for row in self.save_data_result:
                dw.writerow(row)

    def save(self):
        # if data doesn't contain user and volunteers fiels save by using a default user/volunteer
        self.validate()
        serializer_class = DataUploader.get_serializer_class(self.service_type)
        try:
            model_class = DataUploader.get_model_class(self.service_type)
        except KeyError:
            raise InvalidServiceType("Scraping implementation for service type: %s is missing", service_type)
        self.save_data_result = []
        for data in self.validation_data_result:
            if data.get('validation_error'):
                data['save_error'] = "data not valid"
                continue
            name = data.get('name')
            _data = {k:v for k, v in data.items() if k != 'validation_error'}
            try:
                instance = model_class.objects.get(name=name)
                serializer = serializer_class(instance, data=_data, partial=True)
            except Exception:
                serializer = serializer_class(data=_data)
            try:
                serializer.is_valid()
                serializer.save()
                data['save_error'] = "N/A"
            except Exception as E:
                data['save_error'] = E.__repr__
            self.save_data_result.append(data)
        self.create_result_csv()
