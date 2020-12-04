from django.urls import path
from . import views

app_name = 'mytrack'
urlpatterns = [
    path('',views.show_forms, name='forms'),
    path('edit-charge-virale/<str:cv_code>/', views.edit_charge_virale, name='edit_charge_virale'),
    path('respect-rdv/', views.respect_rdv, name="respect_rdv"),
    path('patients-venus/', views.list_is_come, name="is_come"),
    path('rendez-vous/', views.add_rdv, name = "ajout_rdv"),
    path('list-contact/', views.list_rdv, name='list_rdv'),
    path('index-testing/',views.add_index, name="ajout_contact"),
    path('list-index/', views.list_index, name='list_index'),
]
