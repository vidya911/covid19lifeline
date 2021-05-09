from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



from core.models import BasicConfiguration, City, NameBaseConfig, ServiceType, State

GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
)

TICKET_STATUS = (
        ('CREATED', 'CREATED'),
        ('QUEUED', 'QUEUED'),
        ('SOLVED', 'SOLVED'),
        ('UNSOLVED', 'UNSOLVED')
)

class Patient(NameBaseConfig):
    contact_number = models.CharField(max_length=12)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    covid_positive = models.BooleanField(default=True)
    gender = models.CharField(choices=GENDER, max_length=1)
    rfid_no = models.CharField(max_length=32)
    spo2_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    added_by = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"name: {self.name} slug: {self.slug} age: {self.age} gender: {self.gender}"


class HelpTicket(BasicConfiguration):
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    ticket_status = models.CharField(choices=TICKET_STATUS, max_length=10)
    remark = models.TextField(null=True, blank=True)
    remarked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    closed_at = models.DateTimeField()
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Patient name: {self.patient.name} service type: {self.service_type.name} age: {self.patient.age} gender: {self.patient.spo2_level}"


@receiver(post_save, sender=HelpTicket)
def queue_help_ticket(sender, **kwargs):
    """
    on save of HelpTicket, query from database and assign in queue leads
    """
    pass
