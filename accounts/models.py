from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='patient')


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    nid = models.CharField(max_length=10, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    medical_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.user.username} - NID: {self.nid}"


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    contact_number = models.CharField(max_length=11)
    hospital_name = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)

    def __str__(self):
        return f"Doctor: {self.user.username} - Hospital: {self.hospital_name}"