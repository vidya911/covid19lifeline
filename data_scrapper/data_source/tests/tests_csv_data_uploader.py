import os
import json
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from core.models import City, State
from data_scrapper.data_source.csv_data_uploader import DataUploader
from data_scrapper.data_source.tests.utils import get_data_from_csv_file, get_data_from_json_file
from hospital.models import Hospital
from volunteer.models import Volunteer

class DataUploaderHospitalsTest(TestCase):


    @classmethod
    def setUpClass(cls):
        TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

        cls.HOSPITALS_VALID_INVALID_DATA_CSV=os.path.join(TEST_DATA_DIR, "hospitals_valid_invalid_data.csv")
        cls.HOSPITALS_VALID_INVALID_DATA_JSON=os.path.join(TEST_DATA_DIR, "hospitals_valid_invalid_data.json")

        cls.HOSPITALS_ALL_VALID_JSON_DATA=os.path.join(TEST_DATA_DIR, "hospitals_all_valid_json_data.json")
        cls.HOSPITALS_ALL_VALID_CSV_DATA=os.path.join(TEST_DATA_DIR, "hospitals_all_valid_json_data.csv")
        cls.HOSPITALS_ALL_INVALID_JSON_DATA=os.path.join(TEST_DATA_DIR, "hospitals_all_invalid_json_data.json")

        cls.HOSPITALS_WRONG_MANDATORY_HEADERS=os.path.join(TEST_DATA_DIR, "hospitals_wrong_mandatory_headers.csv")
        cls.HOSPITALS_WRONG_NON_MANDATORY_HEADERS=os.path.join(TEST_DATA_DIR, "hospitals_wrong_non_mandatory_headers.csv")

        cls.test_user = User.objects.create(username="test_user")
        cls.test_volunteer_user = User.objects.create(username="test_volunteer")
        cls.test_volunteer = Volunteer.objects.create(name="test_volunteer", user=cls.test_volunteer_user, age=21, volunteer_start_time=datetime.now(), volunteer_end_time=datetime.now())
        cls.state = State.objects.create(name="Bihar")
        cls.city = City.objects.create(name="Patna", state=cls.state)



    def test_upload_from_json_file(self):
        _filename = self.HOSPITALS_ALL_VALID_JSON_DATA
        _instance = DataUploader.upload_from_json_file(_filename, 'hospital')
        self.assertEqual(_instance.service_type, 'hospital')



    def test_upload_from_csv_file(self):
        _filename = self.HOSPITALS_ALL_VALID_CSV_DATA
        _instance = DataUploader.upload_from_csv_file(_filename, 'hospital')
        self.assertEqual(_instance.service_type, 'hospital')


    def test_validate_valid_data_all_fields(self):
        _filename = self.HOSPITALS_ALL_VALID_JSON_DATA
        _instance = DataUploader.upload_from_json_file(_filename, 'hospital')
        self.assertEqual(_instance.service_type, 'hospital')
        _instance.validate()
        validation_data_result = _instance.validation_data_result
        for each in validation_data_result:
            self.assertEqual(each['validation_error'], '')

    def test_save_valid_data_all_fields(self):
        _filename = self.HOSPITALS_ALL_VALID_JSON_DATA
        _instance = DataUploader.upload_from_json_file(_filename, 'hospital')
        _instance.save()
        for each in _instance.save_data_result:
            self.assertEqual(each['save_error'], "N/A")
        for each_obj in _instance.json_data:
            name = each_obj.get('name')
            hospital = Hospital.objects.filter(name=name)
            self.assertGreaterEqual(1, len(hospital))


    def atest_validate_and_save_valid_data_few_fields(self):
        _filename = self.HOSPITALS_ALL_INVALID_JSON_DATA
        _instance = DataUploader.upload_from_json_file(_filename, 'hospital')


    def test_validate_and_save_valid_data_only_mandatory_fields(self):
        """
        """
        pass


    """
    testing for invalid input
    """

    def test_validate_and_save_invalid_data_missing_name(self):
        """

        """
        pass


    def test_validate_and_save_invalid_data_missing_state(self):
        """

        """
        pass


    def test_validate_and_save_invalid_data_missing_city(self):
        """

        """
        pass


    def test_validate_and_save_valid_invalid_data_for_all_json(self):
        """

        """
        pass


    """
    testing populating data from CSV
    """
    def test_validate_and_save_from_csv_correct_headers(self):
        """

        """
        pass


    def test_validate_and_save_from_csv_incorrect_headers(self):
        """

        """
        pass


    def test_validate_and_save_from_csv_ignore_incorrect_headers(self):
        """

        """
        pass


    """
    testing result CSV
    """
    def test_result_csv_creation(self):
        """

        """
        pass


    def test_result_csv_presense_of_validation_error(self):
        """

        """
        pass


    def test_result_csv_presense_of_save_error(self):
        """

        """
        pass


    def test_result_csv_empty_save_validation_error(self):
        """

        """
        pass


    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()
        cls.test_volunteer_user.delete()
        cls.test_volunteer.delete()
