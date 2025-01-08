from rest_framework import serializers
from .models import DoseBooking, CampaignReview


class DoseBookingSerializer(serializers.ModelSerializer):
    dose_date = serializers.DateField(write_only=True)  # Ensure it's required in the input

    class Meta:
        model = DoseBooking
        fields = ['id', 'campaign', 'dose_number', 'dose_date', 'booked_at']
        read_only_fields = ['dose_number', 'booked_at']

    def validate(self, attrs):
        request = self.context['request']
        campaign = attrs['campaign']
        dose_date = attrs['dose_date']

        # Ensure the user is a patient
        if not hasattr(request.user, 'patient_profile'):
            raise serializers.ValidationError("Only patients can book doses.")

        # Ensure the first dose is within the campaign's start and end date
        if not (campaign.start_date <= dose_date <= campaign.end_date):
            raise serializers.ValidationError("The first dose date must be within the campaign's start and end date.")

        # Ensure the patient hasn't already booked this campaign
        if DoseBooking.objects.filter(patient=request.user.patient_profile, campaign=campaign).exists():
            raise serializers.ValidationError("You have already booked a dose for this campaign.")

        return attrs


class DoseViewSerializer(serializers.ModelSerializer):
    campaign = serializers.SerializerMethodField()
    class Meta:
        model = DoseBooking
        fields = ['id', 'patient', 'campaign', 'dose_number', 'dose_date', 'booked_at']
    def get_campaign(self, obj):
        return obj.campaign.campaign_name if obj.campaign else None


class CampaignReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignReview
        fields = ['id', 'campaign', 'review_text', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        request = self.context['request']
        patient = request.user.patient_profile
        campaign = attrs['campaign']

        # Check if the patient has booked a dose for this campaign
        if not DoseBooking.objects.filter(patient=patient, campaign=campaign).exists():
            raise serializers.ValidationError("You can only review campaigns you have booked doses for.")

        # Check if the patient has already reviewed this campaign
        if CampaignReview.objects.filter(patient=patient, campaign=campaign).exists():
            raise serializers.ValidationError("You have already reviewed this campaign.")

        return attrs


class ReviewListSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)

    class Meta:
        model = CampaignReview
        fields = ['patient_full_name', 'review_text', 'created_at']