from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models


from core.models import City, State, NameBaseConfig
from volunteer.models import Volunteer


HOSPITAL_CATEGORY = (
            ('PRIVATE', 'PRIVATE'),
            ('GOVT', 'GOVT'),
            ('NGO', 'NGO'),

)

SOURCE = (
            ('GOOGLE', 'GOOGLE'),
            ('TWITTER', 'TWITTER'),
            ('MANUAL', 'MANUAL'),
            ('OTHERS', 'OTHERS')
)



class Hospital(NameBaseConfig):
    hospital_category = models.CharField(choices=HOSPITAL_CATEGORY, max_length=10, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    hospital_address = models.TextField(blank=True, null=True)
    source = models.CharField(choices=SOURCE, max_length=10, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    # add validator at later stage or make a custom contact number field
    contact_number_1 = models.CharField(max_length=12, blank=True, null=True)
    contact_number_2 = models.CharField(max_length=12, blank=True, null=True)
    contact_number_3 = models.CharField(max_length=12, blank=True, null=True)
    # bed counts
    total_beds_allocated_to_covid = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])

    total_beds_without_oxygen = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])
    available_beds_without_oxygen = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])

    total_beds_with_oxygen = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])
    available_beds_with_oxygen = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])

    total_icu_beds_without_ventilator = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])
    available_icu_beds_without_ventilator = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])

    total_icu_beds_with_ventilator = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])
    available_icu_beds_with_ventilator = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2500)])
    added_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    last_updated_by = models.ForeignKey(Volunteer, blank=True, null=True, on_delete=models.CASCADE)

