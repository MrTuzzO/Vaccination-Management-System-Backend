from datetime import timedelta
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DoseBooking, CampaignReview
from .serializers import DoseBookingSerializer, CampaignReviewSerializer, DoseViewSerializer, ReviewListSerializer
from campaign.models import VaccineCampaign


class DoseBookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DoseBookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            campaign = serializer.validated_data['campaign']
            dose_date = serializer.validated_data['dose_date']
            patient = request.user.patient_profile

            # Create the first dose booking
            first_booking = DoseBooking.objects.create(
                patient=patient,
                campaign=campaign,
                dose_number=1,
                dose_date=dose_date,
            )

            # Automatically generate other doses
            bookings = [first_booking]
            for dose_number in range(2, campaign.vaccine_doses + 1):
                next_dose_date = dose_date + timedelta(days=campaign.dose_interval * (dose_number - 1))
                booking = DoseBooking.objects.create(
                    patient=patient,
                    campaign=campaign,
                    dose_number=dose_number,
                    dose_date=next_dose_date,
                )
                bookings.append(booking)

            # Serialize the created bookings
            response_data = DoseBookingSerializer(bookings, many=True).data
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoseBookingListView(generics.ListAPIView):
    serializer_class = DoseViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = self.request.user.patient_profile
        return DoseBooking.objects.filter(patient=patient).order_by('dose_date')


class DoseBookingDetailView(generics.RetrieveAPIView):
    queryset = DoseBooking.objects.all()
    serializer_class = DoseBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = self.request.user.patient_profile
        return DoseBooking.objects.filter(patient=patient)


class CampaignReviewCreateView(generics.CreateAPIView):
    queryset = CampaignReview.objects.all()
    serializer_class = CampaignReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient_profile)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        campaign_id = self.kwargs.get('pk')
        try:
            campaign = VaccineCampaign.objects.get(id=campaign_id)
        except VaccineCampaign.DoesNotExist:
            raise NotFound(detail="Campaign not found")

        return CampaignReview.objects.filter(campaign=campaign)