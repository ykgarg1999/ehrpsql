from django.urls.conf import path
from . import views

urlpatterns = [
    path('api/doctors/<str:doctorid>/getpatients', views.GetAllPatients.as_view()),
    path('api/doctors/<str:doctorid>/search/<str:search_term>', views.SearchPatient.as_view()),
    path('api/doctors/<str:doctorid>/me', views.meViewSet.as_view()),
    path('api/doctors/<str:doctorid>/addpatient', views.PatientAddViewSet.as_view({"post": "addpatient"})),
    path('api/patients/<str:patientid>/details', views.PatientViewSet.as_view()),
    path('api/patients/<str:patientid>/meds', views.MedicationListViewSet.as_view()),
    path('api/patients/<str:patientid>/<int:medid>', views.MedicationViewSet.as_view()),
    path('api/patients/medications/<int:medid>/dose', views.DosageViewSet.as_view({"get": "dose", "post": "adddose", "patch":"update"})),
    path('api/patients/<str:patientid>/vitaldetails', views.VitalDetailsViewSet.as_view()),
    path('api/patients/<str:patientid>/allergy', views.AllergyDetailsViewSet.as_view()),
    path('api/patient/<str:patientid>/allergy/<int:id>', views.IndAllergyViewSet.as_view()),
    path('api/doctors/<str:patientid>/socialhistory', views.SocialViewSet.as_view()),
    path('api/doctors/<str:patientid>/problems', views.ProblemViewSet.as_view()),
    path('api/doctors/<str:patientid>/problems/<str:id>', views.IndProblemViewSet.as_view()),
    path('api/<str:patientid>/comments',views.CommentViewSet.as_view()),
    path('api/patient/<str:patientid>/comments',views.PatientCommentsViewSet.as_view()),
    path('api/patient/<str:patientid>/me', views.PatientDashboardViewSet.as_view({"get": "me"})),
    path('api/patient/<str:patientid>/vitals', views.PatientVitalDetailsViewSet.as_view()),
    path('api/patient/<str:patientid>/social', views.PatientSocialViewSet.as_view()),
    path('api/patient/<str:patientid>/medications', views.PatientMedicationDetailsViewSet.as_view()),
    path('api/patient/<str:patientid>/allergy', views.PatientAllergyDetailsViewSet.as_view()),
    path('api/patient/<int:medid>/dose/', views.PatientDoseDetailsViewSet.as_view()),
    path('api/patient/<str:patientid>/problem', views.PatientProblemDetailsViewSet.as_view())
]
