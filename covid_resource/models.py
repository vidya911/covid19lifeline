import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models


from core.models import City, State, NameBaseConfig, ResourceType
from volunteer.models import Volunteer


SOURCE = (
            ('GOOGLE', 'GOOGLE'),
            ('TWITTER', 'TWITTER'),
            ('MANUAL', 'MANUAL'),
            ('OTHERS', 'OTHERS')
)


class Resource(NameBaseConfig):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    hospital_address = models.TextField(blank=True, null=True)
    source = models.CharField(choices=SOURCE, max_length=10, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    # add validator at later stage or make a custom contact number field
    contact_number = models.CharField(max_length=12, blank=True, null=True)
    alternate_contact_number = models.CharField(max_length=12, blank=True, null=True)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.DO_NOTHING)
    #TODO: write property named state to get the state name
    resource_availibity_description  = models.TextField(blank=True, null=True)
    resource_availibity = models.BooleanField(default=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_mobile_number = models.BooleanField(default=False)
