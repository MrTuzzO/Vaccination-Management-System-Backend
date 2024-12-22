from django.db import models
from campaign.models import VaccineCampaign
from accounts.models import Patient


class DoseBooking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dose_bookings')
    campaign = models.ForeignKey(VaccineCampaign, on_delete=models.CASCADE, related_name='dose_bookings')
    dose_number = models.PositiveIntegerField()
    dose_date = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} - {self.campaign.campaign_name} - Dose {self.dose_number}"


class CampaignReview(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='campaign_reviews')
    campaign = models.ForeignKey(VaccineCampaign, on_delete=models.CASCADE, related_name='campaign_reviews')
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.patient.user.username} for {self.campaign.campaign_name}"
