from django import forms
from .models import SiteInfo

class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = ['site_code', 'site_name', 'service', 'district', 'region', 'direction_region']
        widgets = {
            'site_code': forms.TextInput(attrs={"id": "site_code","class": "form-control","placeholder": "Code du site",}),

            'site_name': forms.TextInput(attrs={"id": "site_name", 'name':'site_name', "class": "form-control","placeholder": "Nom du site",}),

            'region': forms.TextInput(attrs={"id": "region", "class": "form-control","placeholder": "Region sanitaire",}),

            'district': forms.TextInput(attrs={"id": "district","class": "form-control","placeholder": "District sanitaire",}),

            'service': forms.TextInput(attrs={"id": "service","class": "form-control","placeholder": "Nom du service",}),

            'direction_region': forms.TextInput(attrs={"id": "direction_sanitaire", "class": "form-control","placeholder": "Direction sanitaire",}),
        }

        labels = {
            'site_name': 'Nom du site',
            'site_code': 'Code du site',
            'region': 'Région sanitaire',
            'district': 'Disctrict sanitaire',
            'service': 'Nom du service',
            'direction_region': 'Direction régionanle',
        }