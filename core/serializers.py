from rest_framework import serializers

from core.models import City, State
from django.contrib.auth.models import User


class StateSerializer(serializers.ModelSerializer):

     class Meta:
        model = State
        fields = ['name']

     def to_representation(self, value):
        return str(self.value)

class CitySerializer(serializers.ModelSerializer):

     class Meta:
        model = City
        fields = ['name']


class UserSerializer(serializers.PrimaryKeyRelatedField):

     class Meta:
        model = User
        fields = ['username']

