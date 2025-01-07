from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VaccineCampaign
from .serializers import VaccineCampaignSerializer
from .permissions import IsAuthorOrReadOnly, IsDoctor
from rest_framework.permissions import IsAuthenticated


class VaccineCampaignList(APIView):
    permission_classes = [IsDoctor]

    def get(self, request, format=None):
        vaccineList = VaccineCampaign.objects.all()
        serializer = VaccineCampaignSerializer(vaccineList, many= True)
        return Response(serializer.data)

    def post(self, request, format = None):
        doctor_profile = getattr(request.user, "doctor_profile", None)
        if not doctor_profile:
            return Response(
                {"detail": "Only doctors can create vaccine campaigns."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = VaccineCampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=doctor_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VaccineCampaignDetail(APIView):

    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return VaccineCampaign.objects.get(pk=pk)
        except VaccineCampaign.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        vaccine = self.get_object(pk)
        serializer = VaccineCampaignSerializer(vaccine)
        return Response(serializer.data)

    def put(self, request,pk, format=None):
        vaccine = self.get_object(pk)
        serializer = VaccineCampaignSerializer(vaccine, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk, format=None):
        vaccine = self.get_object(pk)
        vaccine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorCampaignList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.user_type != 'doctor':
            return Response({'detail': 'Permission Denied'}, status=403)

        doctor = request.user.doctor_profile
        campaigns = VaccineCampaign.objects.filter(doctor=doctor)
        serializer = VaccineCampaignSerializer(campaigns, many=True)
        return Response(serializer.data)