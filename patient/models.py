from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models


from core.models import NameBaseConfig, ServiceType

GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
)

class Patient(NameBaseConfig):
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    covid_positive = models.BooleanField(default=True)
    gender = models.CharField(choices=GENDER, max_length=1)
    rfid_no = models.CharField(max_length=32)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    spo2_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    added_by = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"name: {self.name} slug: {self.slug} age: {self.age} gender: {self.gender}"

