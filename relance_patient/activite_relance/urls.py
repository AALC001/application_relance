from django.urls import path
from .views import GeneratePDF
from . import views

app_name = "activite_relance"

urlpatterns = [
    path('list-site-relance/', views.list_site_relance, name='list_site_relance'),
    path('list-relance/', views.list_relance, name='list_relance'),
    path('add-relance/', views.add_relance, name="add_relance"),
    path('edit-relance/<str:relance_code>/', views.edit_relance, name="edit_relance"),
    path('archive-relance/<str:relance_code>/', views.archive_relance, name="archive_relance"),
    path("export-fiche-relance/", GeneratePDF.as_view(), name="export_fiche_relance"),
]
