from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models


from core.models import NameBaseConfig, ServiceType

GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
)

class Volunteer(NameBaseConfig):
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    gender = models.CharField(choices=GENDER, max_length=1)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    on_call = models.BooleanField(default=False)
    volunteer_start_time = models.TimeField()
    volunteer_end_time = models.TimeField()

    def __str__(self):
        return f"name: {self.name} slug: {self.slug} age: {self.age} gender: {self.gender}"

