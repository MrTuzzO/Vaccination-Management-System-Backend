from django.urls import path
from .views import CustomPatientRegisterView, PatientProfileUpdateView, CustomLoginView, UserProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registration/', CustomPatientRegisterView.as_view(), name='custom-register'),
    path('profile/update/', PatientProfileUpdateView.as_view(), name='update-profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
