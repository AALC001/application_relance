import json
from pdb import set_trace
from django.db import models
from django.utils import timezone
from authentication.models import Account
from dashboard.models import SiteInfo

# Create your models here.

statut_matrimonial = [
    ('marie','marié(e)'),
    ('celibataire','celibataire'),
    ('concubinage', 'concubinage'),
    ('veuf','veuf(ve)'),
    ('divorce','divorcé(e)')
]


class FicheRelance(models.Model):
    info_relance = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        relances = json.loads(self.info_relance)
        return str(len(relances))

# Model du patient
class Patient(models.Model):
    site = models.ForeignKey(SiteInfo, on_delete = models.CASCADE)
    code_patient = models.CharField(max_length=155)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    sexe = models.CharField(max_length=10)
    age = models.CharField(max_length=5, default = None)
    situation_matrimoniale = models.CharField(max_length = 20,choices = statut_matrimonial, default='celibataire')
    contact = models.CharField(max_length=30)
    domicile = models.CharField(max_length=60)

    #  # Patient next rdv
    # def next_rdv(self):
    #     rdv_arv = self.daterdv.date_proch_arv
    #     rdv_cv = self.daterdv.date_proch_cv

    #     if rdv_cv > rdv_arv:
    #         return {"rdv_type": "cv", "rdv_date" : rdv_cv}
    #     return {"rdv_type": "arv", "rdv_date" : rdv_arv}
        
        
    def __str__(self):
        return f'<Patient({self.code_patient})> {self.first_name} {self.last_name}'

# Model Personne de soutient du patient
class PersonSoutien(models.Model):
    patient = models.OneToOneField(Patient, on_delete = models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    lien = models.CharField(max_length=100, verbose_name='lien avec le patient')

    def __str__(self):
        return f"<Person Soutien>{self.first_name} {self.last_name}"
    

# Model date RDV et prochain RDV
class DateRDV(models.Model):
    patient = models.OneToOneField(Patient, on_delete = models.CASCADE, primary_key=True)
    date_last_arv = models.DateField(verbose_name='Date de dispensation Anti Retro-Viraux')
    date_proch_arv = models.DateField(verbose_name='Date de prochain rendez-vous ARV')
    date_last_cv = models.DateField(verbose_name='Date de dernier examen Charge Virale')
    date_proch_cv = models.DateField(verbose_name='Date de prochain examen Charge Virale')

    def __str__(self):
        return f"<Date RDV({self.patient.first_name} {self.patient.last_name})> prochain ARV => {self.date_proch_arv} prochain CV => {self.date_proch_cv}"
    

class Venue(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key= True)
    info_rdv = models.TextField()

# Model type d'examen du patient pour le RDV
# class ExamenCV(models.Model):
#     nbre_CD4 = models.CharField(max_length = 15,verbose_name='nombre par mm3 ou pourcentage')
#     copie_cv = models.CharField(max_length=15,verbose_name='nombre de copie par ml')
#     patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
