from django.contrib import admin
from .models import PatientDetails, Allergy, VitalDetails, Medication, Dosage, ProblemDetails, SocialHistory
# Register your models here.

admin.site.register(PatientDetails)
admin.site.register(Allergy)
admin.site.register(VitalDetails)
admin.site.register(Medication)
admin.site.register(Dosage)
admin.site.register(ProblemDetails)
admin.site.register(SocialHistory)