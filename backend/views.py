from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from accounts.models import Profile
from rest_framework.authentication import get_authorization_header
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import PatientDetails, VitalDetails, Allergy, Medication, Dosage, ProblemDetails, SocialHistory, PatientComments
import uuid
from .serializers import CommentSerializer, PatientDetailsSerializer, VitalDetailsSerializer, AllergySerializer, MedicationSerializer, \
    DosageSerializer, ProblemDetailsSerializer, SocialHistorySerializer, PatientDashboardSerializer, \
    DoctorDashboardSerializer, DoctorDetailsSerializer
from rest_framework import status, exceptions
from rest_framework.permissions import AllowAny
from backend import serializers
from .utils import Util
from django.conf import settings
import jwt


def getToken(request, doctorid=None, patientid=None):
    auth_header = get_authorization_header(request)
    auth_data = auth_header.decode('utf-8')
    auth_token = auth_data.split(" ")
    if len(auth_token) != 2:
        raise exceptions.AuthenticationFailed("Token not valid")
    token = auth_token[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        userid = str(payload['user'])
        if doctorid is not None:
            doctorid = str(doctorid)
            if userid == doctorid:
                return token
            return None
        else:
            doctor = str(PatientDetails.objects.get(id=patientid).doctor.id)
            if userid == doctor:
                return token
            return None
    except jwt.ExpiredSignatureError as ex:
        raise exceptions.AuthenticationFailed("Token is expired,login again")
    except jwt.DecodeError as ex:
        raise exceptions.AuthenticationFailed("Token is invalid")

    except Profile.DoesNotExist as no_users:
        raise exceptions.AuthenticationFailed("No such user")


from accounts.models import User


class GetAllPatients(APIView):
    def get(self, request, doctorid):

        serializer_class = PatientDetailsSerializer
        try:
            patients = PatientDetails.objects.filter(doctor=doctorid)
            token = getToken(request, doctorid, None)
            if token is None:
                content = {'Invalid token'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            return Response(PatientDetailsSerializer(patients, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Patient not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class IndAllergyViewSet(APIView):
    def delete(self, request, patientid, id):
        patientid = uuid.UUID(patientid)
        id = int(id)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            allergydetail = Allergy.objects.get(pk=id)
            allergydetail.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            content={'Allergy not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, patientid, id):
        patientid = uuid.UUID(patientid)
        print("100 line number")
        id = int(id)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        allergydetail = Allergy.objects.get(pk=id)

        data = request.data
        data['patient'] = patientid
        serializer = AllergySerializer(allergydetail, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllergyDetailsViewSet(APIView):

    def get(self, request, patientid):
        serializer_class = AllergySerializer
        patientid = uuid.UUID(patientid)
        patient = None

        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            token = getToken(request, None, patientid)
            if token is None:
                content = {'Invalid token'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            allergydetails = Allergy.objects.filter(patient=patient)
            return Response(AllergySerializer(allergydetails, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Allergy details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, patientid):
        serializer_class = AllergySerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['patient'] = patientid
        serializer = AllergySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VitalDetailsViewSet(APIView):
    def get(self, request, patientid):
        serializer_class = VitalDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            vitaldetails = VitalDetails.objects.get(patient=patient)
            return Response(VitalDetailsSerializer(vitaldetails).data, status=status.HTTP_200_OK)
        except:
            content = {'Vital details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, patientid):
        serializer_class = VitalDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            vitaldetails = VitalDetails.objects.get(patient=patient)
            data = request.data
            data['patient'] = patientid
            serializer = VitalDetailsSerializer(vitaldetails, data=data)
            print(vitaldetails)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            data = request.data
            data['patient'] = patientid
            print(data)
            serializer = VitalDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchPatient(APIView):
    def get(self, request, doctorid, search_term):
        token = getToken(request, doctorid, None)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Profile.objects.get(pk=doctorid)
            patient = PatientDetails.objects.filter(doctor=doctor)
            patient = PatientDetails.objects.filter(doctor=doctor).filter(name__icontains=search_term)
            serializer = DoctorDashboardSerializer(patient, many=True)
            return Response(serializer.data)
        except:
            return Response({'Doctor not found for this id'}, status=status.HTTP_400_BAD_REQUEST)


class meViewSet(APIView):
    def get(self, request, *args, **kwargs):
        target_user = uuid.UUID(kwargs['doctorid'])
        token = getToken(request, target_user, None)
        print("line number 238", token)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Profile.objects.get(id=target_user)
            print("id", target_user)
            serializer = DoctorDetailsSerializer(doctor)
            data = serializer.data
            print(data)
            doctor_id = data['id']
            user = User.objects.get(profile=doctor_id)
            name = user.first_name + " " + user.last_name
            data['doctor_name'] = name
            data['doctor_email'] = user.email

            return Response(data, status=status.HTTP_200_OK)
        except:
            content = {"Doctor Not Found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class PatientAddViewSet(ModelViewSet):
    queryset = PatientDetails.objects.all()
    serializer_class = PatientDetailsSerializer

    @action(methods=['post'], detail=True)
    def addpatient(self, request, *args, **kwargs):
        target_user = uuid.UUID(kwargs['doctorid'])

        token = getToken(request, target_user, None)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['doctor'] = target_user

        serializer = PatientDetailsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = PatientDetails.objects.get(email_id=user_data['email_id'])
            print(user)
            email_body = 'Welcome {} To The Online EHR \n \n Please use the below credential for login \n'.format(
                user.name) + str(
                user.id) + " " + 'use only for personal Use'
            data = {
                'email_body': email_body,
                'email_subject': 'Login credential For Online EHR'
            }
            # Util.sent_email(data, user_data['email_id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientViewSet(APIView):
    def get(self, request, patientid):
        serializer_class = PatientDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
            return Response(PatientDetailsSerializer(patient).data, status=status.HTTP_200_OK)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, patientid):
        serializer_class = PatientDetailsSerializer
        patientid = uuid.UUID(patientid)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
            serializer = PatientDetailsSerializer(patient, data=request.data)
            # print(vitaldetails)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class MedicationViewSet(APIView):
    def patch(self, request, patientid, medid):
        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # patient = PatientDetails.objects.get(id=patientid)
            med = Medication.objects.get(id=medid)            
            data = request.data
            data['patient'] = patientid
            serializer = MedicationSerializer(med, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'Medication not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, patientid, medid):
        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = PatientDetails.objects.get(id=patientid)
            meds = Medication.objects.get(id=medid)
            meds.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            content = {"Not found"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class MedicationListViewSet(APIView):
    def get(self, request, patientid):
        serializer_class = MedicationSerializer
        patientid = uuid.UUID(patientid)

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientDetails.objects.get(id=patientid)
            meds = Medication.objects.filter(patient=patient)
            serializer = MedicationSerializer(meds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            content = {"Not found"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, patientid):

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['patient'] = patientid
        serializer = MedicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DosageViewSet(ModelViewSet):
    queryset = Dosage.objects.all()
    serializer_class = DosageSerializer
    
    @action(methods=['get'], detail=True)
    def dose(self, request, *args, **kwargs):
        target_user = int(kwargs['medid'])
        try:
            medication = Medication.objects.get(pk=target_user)
            dosy = Dosage.objects.get(medication=medication)
            serializer = DosageSerializer(dosy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            content = {"Not found"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        target_user = int(kwargs['medid'])
        
        try:
            medication = Medication.objects.get(pk=target_user)
            dosage = Dosage.objects.get(medication=medication)
            data = request.data
            data['medication'] = target_user
            serializer = DosageSerializer(dosage, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'No medication found'}
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def adddose(self, request, *args, **kwargs):
        target_user = int(kwargs['medid'])
        data = request.data
        data['medication'] = target_user
        serializer = DosageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProblemViewSet(APIView):
    def get(self, request, patientid):
        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = ProblemDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            problemdetails = ProblemDetails.objects.filter(patient=patient)
            return Response(ProblemDetailsSerializer(problemdetails, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Problem details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, patientid):
        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = ProblemDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
            data = request.data
            data['patient'] = patientid
            serializer = ProblemDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class IndProblemViewSet(APIView):
    def patch(self, request, patientid, id):

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = ProblemDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            problem = ProblemDetails.objects.get(id=id)
            data = request.data
            data['patient'] = patientid
            serializer = ProblemDetailsSerializer(problem, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, patientid, id):
        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = ProblemDetailsSerializer
        patientid = uuid.UUID(patientid)
        try:
            problem = ProblemDetails.objects.get(id=id)
            problem.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            content = {"Not found"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SocialViewSet(APIView):
    def get(self, request, patientid):

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = SocialHistorySerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            socialdetails = SocialHistory.objects.get(patient=patient)
            return Response(SocialHistorySerializer(socialdetails).data, status=status.HTTP_200_OK)
        except:
            content = {'social details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, patientid):

        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = SocialHistorySerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            socialdetails = SocialHistory.objects.get(patient=patient)
            data = request.data
            data['patient'] = patientid
            serializer = SocialHistorySerializer(socialdetails, data=data)
            # print(vitaldetails)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            data = request.data
            data['patient'] = patientid
            print(data)
            serializer = SocialHistorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentViewSet(APIView):

    def get(self,request, patientid):
        token = getToken(request, None, patientid)
        if token is None:
            content = {'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            comments = PatientComments.objects.filter(patient=patient)
            print("THESE ARE THE COMMENTS",comments)
            return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Problem details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)



class PatientDashboardViewSet(RetrieveModelMixin, GenericViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        queryset = PatientDetails.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientDashboardSerializer

    @action(detail=True, methods=["GET", "PUT"])
    def me(self, request, *args, **kwargs):
        Patient = get_object_or_404(PatientDetails, pk=self.kwargs['patientid'])
        serializer = PatientDetailsSerializer(Patient)
        data = serializer.data
        doctor_id = data['doctor']
        user = User.objects.get(profile=doctor_id)
        name = user.first_name + " " + user.last_name

        data['doctor_name'] = name

        return Response(data)


class PatientVitalDetailsViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patientid):
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            vitaldetails = VitalDetails.objects.get(patient=patient)
            return Response(VitalDetailsSerializer(vitaldetails).data, status=status.HTTP_200_OK)
        except:
            content = {'Vital details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class PatientCommentsViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request, patientid):
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['patient'] = patientid
        print(data)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PatientMedicationDetailsViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patientid):
        serializer_class = MedicationSerializer
        patientid = uuid.UUID(patientid)
        try:
            patient = PatientDetails.objects.get(id=patientid)
            meds = Medication.objects.filter(patient=patient)
            serializer = MedicationSerializer(meds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            content = {"Not found"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PatientSocialViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patientid):
        serializer_class = SocialHistorySerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            socialdetails = SocialHistory.objects.get(patient=patient)
            return Response(SocialHistorySerializer(socialdetails).data, status=status.HTTP_200_OK)
        except:
            content = {'social details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class PatientAllergyDetailsViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patientid):
        serializer_class = AllergySerializer
        patientid = uuid.UUID(patientid)
        patient = None

        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            allergydetails = Allergy.objects.filter(patient=patient)
            return Response(AllergySerializer(allergydetails, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Allergy details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class PatientDoseDetailsViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, medid):
        try:
            medication = Medication.objects.get(pk=medid)
            dose = Dosage.objects.get(medication=medication)
            serializer = DosageSerializer(dose)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            content = {"Not found"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PatientProblemDetailsViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patientid):
        serializer_class = ProblemDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            problemdetails = ProblemDetails.objects.filter(patient=patient)
            return Response(ProblemDetailsSerializer(problemdetails, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Problem details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
