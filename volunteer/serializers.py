from rest_framework import serializers

from core.serializers import UserSerializer
from django.contrib.auth.models import User

from volunteer.models import Volunteer

class VolunteerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Volunteer
        fields = ['user']

