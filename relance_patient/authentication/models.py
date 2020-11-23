import secrets
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import dashboard.models as dash_model

class AccountManager(BaseUserManager):
    def create_user(self, email, password = None):

        if not email:
            raise ValueError('Email must be provided')
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.token =secrets.token_hex(32)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password = None):
        user = self.create_user(
            email,
            password = password,
            )
        user.is_super = True
        user.is_active = True
        user.is_admin=True
        user.is_staff = True
        user.save(
            using = self._db
        )
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',max_length=255, unique=True)
    token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    first_connection = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f'Email : {self.email}'

    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def _get_account_site(self):
        return dash_model.SiteInfo.objects.filter(site_code=self.user.site_code).first()

    @property
    def account_site_file_loaded(self):
        site = self._get_account_site
        if site and site.patient_file:
            return True
        return False

        
class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    site_code = models.CharField(max_length=100, default="")
    user_code = models.CharField(max_length=250, unique=True)
    last_name = models.CharField(verbose_name='Last name',max_length = 70)
    first_name = models.CharField(verbose_name='First name',max_length = 70)
    contact = models.CharField(verbose_name='Contact',max_length = 70, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Nom : {self.last_name} ; Prénom : {self.first_name}'