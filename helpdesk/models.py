from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from core.models import BasicConfiguration
from hospital.models import Hospital
from volunteer.models import Volunteer



class LeadStatus(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(LeadStatus, self).save(*args, **kwargs)


class LeadRemark(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(LeadRemark, self).save(*args, **kwargs)


# HospitalLeads

class HospitalLead(BasicConfiguration):
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.DO_NOTHING)
    hospital = models.ForeignKey(Hospital, on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING)
    lead_remark = models.ForeignKey(LeadRemark, on_delete=models.DO_NOTHING)
    priority_point = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(100)])
    time_taken = models.FloatField()
    comment = models.TextField(null=True, blank=True)
