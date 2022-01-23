from pyexpat import model
from django.db.models import fields
from rest_framework import serializers
from .models import *


class ChoicesSerializerField(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        method_name = 'get_{field_name}_display'.format(field_name=self.field_name)
        # retrieve instance method
        method = getattr(value, method_name)
        # finally use instance method to return result of get_XXXX_display()
        return method()


class PatientDetailsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = PatientDetails
        fields = '__all__'


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'


class VitalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalDetails
        fields = '__all__'


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class DosageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosage
        fields = '__all__'


class ProblemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemDetails
        fields = '__all__'


class SocialHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialHistory
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)

    class Meta:
        model = PatientComments
        fields = '__all__'


class SimpleDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'speciality']


class SimpleProblemPatient(serializers.ModelSerializer):
    class Meta:
        model = ProblemDetails
        fields = ['problem_name', 'start_date', 'end_date']


class PatientDashboardSerializer(serializers.ModelSerializer):
    doctor = SimpleDoctorSerializer()
    problem_patient = SimpleProblemPatient(many=True)

    class Meta:
        model = PatientDetails
        fields = ['doctor', 'problem_patient']


class DoctorDashboardSerializer(serializers.ModelSerializer):
    problem_patient = SimpleProblemPatient(many=True)

    class Meta:
        model = PatientDetails
        fields = ['id', 'name', 'problem_patient']


class DoctorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'gender', 'speciality']
