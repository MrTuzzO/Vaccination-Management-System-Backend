from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Patient, CustomUser, Doctor
from dj_rest_auth.serializers import LoginSerializer
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# class CustomLoginSerializer(LoginSerializer):
#     username = serializers.CharField(required=False, allow_blank=True)
#     email = serializers.EmailField(required=False, allow_blank=True)
#     password = serializers.CharField(style={'input_type': 'password'})
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         email = attrs.get('email')
#         if not username and not email:
#             raise serializers.ValidationError("Either username or email must be provided.")
#         return super().validate(attrs)



class CustomPatientRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    nid = serializers.CharField(max_length=10, required=True)
    age = serializers.IntegerField(required=True)
    medical_info = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def validate_nid(self, value):
        if Patient.objects.filter(nid=value).exists():
            raise ValidationError("A patient with this NID already exists.")
        return value

    def save(self, request):
        # Perform validations
        self.validate_email(self.validated_data.get("email"))
        self.validate_nid(self.validated_data.get("nid"))

        # Save the user instance using the parent serializer
        user = super().save(request)
        user.user_type = 'patient'
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

        # Create the associated Patient profile
        Patient.objects.create(
            user=user,
            nid=self.validated_data['nid'],
            age=self.validated_data['age'],
            medical_info=self.validated_data.get('medical_info', '')
        )

        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'age', 'medical_info']

    def validate_email(self, value):
        # Check if email is unique
        user = self.instance.user
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        # Update fields related to the User model
        user_data = validated_data.pop('user', {})
        for field, value in user_data.items():
            setattr(instance.user, field, value)

        # Update fields related to the Patient model
        for field, value in validated_data.items():
            setattr(instance, field, value)

        # Save both user and patient instances
        instance.user.save()
        instance.save()
        return instance


#------------username or pemail------------------
class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        if not username_or_email or not password:
            raise serializers.ValidationError("Username/email and password are required.")

        # Determine if the input is a valid email
        is_email = False
        try:
            validate_email(username_or_email)
            is_email = True
        except ValidationError:
            pass

        if is_email:  # If valid email, find user by email
            try:
                user = CustomUser.objects.get(email=username_or_email)
                username = user.username  # Retrieve the username for authentication
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")
        else:  # Treat input as a username
            username = username_or_email

        # Authenticate the user
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        attrs['user'] = user
        return attrs


# --------------for profile details
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type']


class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'id', 'nid', 'age', 'medical_info']


class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'id', 'contact_number', 'hospital_name', 'speciality']


class UserProfileSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user_type == 'patient' and hasattr(obj, 'patient_profile'):
            return PatientSerializer(obj.patient_profile).data
        elif obj.user_type == 'doctor' and hasattr(obj, 'doctor_profile'):
            return DoctorSerializer(obj.doctor_profile).data
        return None