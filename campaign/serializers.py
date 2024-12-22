from rest_framework import serializers
from accounts.models import Doctor
from .models import VaccineCampaign


class VaccineCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = VaccineCampaign
        fields = [
            'id', 'campaign_name', 'description', 'start_date', 'end_date',
            'vaccine_type', 'vaccine_doses', 'dose_interval',
            'available_vaccines', 'doctor'
        ]
