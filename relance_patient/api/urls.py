from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('rdv/', views.ListRDV.as_view(), name="listing_rdv"),
    path('patient/count/', views.count_patient, name='patient_count'),
]
