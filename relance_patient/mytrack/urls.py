from django.urls import path
from . import views

app_name = 'mytrack'
urlpatterns = [
    path('',views.show_forms, name='forms'),
    path('respect-rdv/', views.respect_rdv, name="respect_rdv"),
    path('patients-venus/', views.list_is_come, name="is_come"),
    path('rendez-vous/', views.add_rdv, name = "ajout_rdv"),
    path('modif-rdv/<str:code_rdv>/',views.edit_rdv, name="edit_rdv"),
    path('list-rdv/', views.list_rdv, name='list_rdv'),
    path('index-testing/',views.add_index, name="ajout_contact"),
    path('modif-index/<str:code_index>/', views.edit_index, name="edit_index"),
    path('list-index/', views.list_index, name='list_index'),
]
