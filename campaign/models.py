from django.db import models
from django.conf import settings
from accounts.models import Doctor


class VaccineCampaign(models.Model):
    campaign_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    vaccine_type = models.CharField(max_length=255)  # Example: 'COVID-19', 'Flu', etc.
    vaccine_doses = models.PositiveIntegerField(default=1)  # Number of doses in the campaign
    dose_interval = models.PositiveIntegerField(default=28)  # Interval in days between doses
    available_vaccines = models.PositiveIntegerField()  # Number of vaccines available for the campaign
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,  related_name='created_campaigns', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.campaign_name
