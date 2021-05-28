from rest_framework import serializers
from django.contrib.auth.models import User


from core.serializers import CitySerializer, StateSerializer, UserSerializer
from core.models import City, State
from covid_resource.models import Resource
from volunteer.models import Volunteer
from volunteer.serializers import VolunteerUserSerializer


class ResourceSerializer(serializers.ModelSerializer):
     city = serializers.CharField(source="city.name")
     state = serializers.CharField(source="state.name")

     class Meta:
        model = Resource
        exclude = ['id', 'slug', 'active', 'unique_id']

     def to_internal_value(self, data):
        data = super().to_internal_value(data)
        city_name = data['city']['name']
        try:
            _city = City.objects.get(name=city_name)
        except Exception:
            self.fail('invalid_city_name', data_type=type(city_name).__name__)
        else:
            data['city'] = _city
        return data
