import datetime
import json
#from dateutil import relativedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
#from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from string import ascii_uppercase, digits
import re
from authentication.models import Account
from dashboard.models import SiteInfo
# Create your models here.

# class ChargeVirale(models.Model):
#     # code_patient = models.ForeignKey("Patient", 
#     #             on_delete=models.CASCADE, blank=True, null=True, related_name="charge_virale")
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     info_charge_virale = models.TextField()

#     def __str__(self):
#         cv = json.loads(self.info_charge_virale)
#         return str(len(cv))
    

class Respect(models.Model):
    info_respect_rdv = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        respect = json.loads(self.info_respect_rdv)
        return str(len(respect))



class FicheIndex(models.Model):
    info_index = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        index = json.loads(self.info_index)
        return str(len(index))



class FicheRdv(models.Model):
    info_rdv = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        rdv = json.loads(self.info_rdv)
        return str(len(rdv))