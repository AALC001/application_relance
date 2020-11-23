from django.db import models
from authentication.models import Account
class PatientListing(models.Model):
    account = models.ManyToManyField(Account)
    site_code = models.CharField(verbose_name="site_code", max_length=255)
    listing_file = models.URLField(blank=True)
    listing = models.TextField(verbose_name="Listing", blank=True)
    state = models.CharField(max_length=10, default='actif')

    def __str__(self):
        return f"{self.site_code} {self.account.email}"