from dj_rest_auth.registration.views import RegisterView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import CustomPatientRegisterSerializer, PatientProfileSerializer, UserProfileSerializer
from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from campaign.permissions import IsPatient

class CustomPatientRegisterView(RegisterView):
    serializer_class = CustomPatientRegisterSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class PatientProfileUpdateView(UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated & IsPatient]

    def get_object(self):
        return self.request.user.patient_profile


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)