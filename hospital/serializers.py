from rest_framework import serializers
from django.contrib.auth.models import User


from core.serializers import CitySerializer, StateSerializer, UserSerializer
from core.models import City, State
from hospital.models import Hospital
from volunteer.models import Volunteer
from volunteer.serializers import VolunteerUserSerializer


class HospitalJSONSerializer(serializers.ModelSerializer):
     state = serializers.CharField(source="state.name")
     city = serializers.CharField(source="city.name")
     added_by = serializers.PrimaryKeyRelatedField(read_only=True)
     last_updated_by = serializers.PrimaryKeyRelatedField(read_only=True)

     class Meta:
        model = Hospital
        exclude = ['id', 'slug', 'active']

     def to_internal_value(self, data):
        data = super().to_internal_value(data)
        state_name = data['state']['name']
        try:
            _state = State.objects.get(name=state_name)
        except Exception:
            self.fail('invalid_state_name', data_type=type(state_name).__name__)
        else:
            data['state'] = _state

        city_name = data['city']['name']
        try:
            _city = City.objects.get(name=city_name, state=_state)
        except Exception:
            self.fail('invalid_city_name', data_type=type(city_name).__name__)
        else:
            data['city'] = _city

#        added_by = data['user']['username']
#        try:
#            added_by_user = User.objects.get(username=added_by)
#        except Exception:
#            self.fail('invalid_added_by', data_type=type(added_by).__name__)
#        else:
#            data['added_by'] = added_by_user
#
#        last_updated_by_volunteer = data['volunteer']['user']['username']
#        try:
#            volunteer = Volunteer.objects.get(user_username=last_updated_by_volunteer)
#        except Exception:
#            self.fail('invalid_last_updated_by', data_type=type(city_name).__name__)
#        else:
#            data['last_updated_by'] = volunteer
        return data
