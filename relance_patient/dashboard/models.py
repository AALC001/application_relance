import authentication.models as auth_model
from django.db import models
# from authentication.models import Account


# Model info site
class SiteInfo(models.Model):
    site_code = models.CharField(max_length=100, unique=True)
    site_name = models.CharField(max_length=100)
    service = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    direction_region = models.CharField(max_length=30)
    patient_file = models.CharField(max_length=150, blank=True)
    
    def __str__(self):
        return self.site_name

    # Get site admin
    @property
    def site_admin(self):
        accounts = auth_model.Account.objects.filter(is_admin=True, is_super=False)
        for account in accounts:
            if self.site_code == account.user.site_code:
                return account
        return None
