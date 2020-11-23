import locale
from datetime import datetime
from django.shortcuts import render, reverse
from django.http import JsonResponse
from django.utils import timezone
from .models import SiteInfo
from authentication.models import Account, User
from .forms import SiteInfoForm
from authentication.models import Account
from activite_relance.models import Patient, FicheRelance
from activite_relance.views import load_relance_list
from relance_patient.utils import get_year_month


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))


def count_users_by_site(site_code):
    users = Account.objects.all()
    return len([user for user in users if user.user.site_code == site_code ])

def count_patients_by_site(site_code):
    patients =  Patient.objects.all()
    return len([patient for patient in patients if patient.site.site_code == site_code])


def get_site_relance(request):
    fiche_relance = FicheRelance.objects.all()
    site_user_relance = []
    relances = []

    for fiche in fiche_relance:
        if fiche.account.user.site_code == request.user.user.site_code:
            site_user_relance.append(fiche)
   
    if site_user_relance:
        for site_fiche in site_user_relance:
            relance_user = site_fiche.account

            for relance in load_relance_list(site_fiche.info_relance):
                relance['owner'] = f"{relance_user.user.first_name} {relance_user.user.last_name}"
                relance['relance_date'] = datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
                relances.append(relance)

    filtered_relances = list(filter(lambda x:  x['relance_date'], relances))
    return filtered_relances
        

# Dashboard Home
# @login_required(login_url='/auth/login')
def home(request):
    len_account = count_users_by_site(request.user.user.site_code)
    locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
    len_patient = 0
    relances = get_site_relance(request)

    context = {
        'date': timezone.localdate().year,
        'len_account': len_account,
        'len_patient': len_patient,
        'relances': relances[:3],
        'len_relance': len(relances),
        'patient_url': reverse('api:patient_count'),
    }
    return render(request, 'dashboard/home.html', context)


def site_list(request):
    sites = SiteInfo.objects.all()
    accounts = Account.objects.filter(is_admin=True, is_super=False)
    users = []
    for account in accounts:
        users.append(account.user.site_code)

    context = {
        'sites': sites,
        'accounts': accounts
    }
    return render(request, 'dashboard/site_list.html', context)

def site_create(request):
    if request.method == 'POST':
        form_data = request.POST
        form = SiteInfoForm(form_data)
        
        if form.is_valid():
            form.save()

        link = reverse('dashboard:site_list')

        return JsonResponse({
            'status': 200,
            'type': 'success',
            'message': "Le site a été créé", 
            'redirectLink': {
                'link': link,
            }, 
        })

    form = SiteInfoForm(use_required_attribute=False)
    context = {'form': form}
    return render(request, 'dashboard/site_create.html', context)


def site_edit(request, pk):
    site = SiteInfo.objects.get(pk=pk)

    if request.method == 'POST':
        form_data = request.POST
        form = SiteInfoForm(form_data, instance=site)

        if form.is_valid():
            form.save()

            link = reverse('dashboard:site_list')
            return JsonResponse({
                'status': 200,
                'type': 'success',
                'message': "Le site a été modifié", 
                'redirectLink': {
                    'link': link,
                }, 
            })
        else:
            return JsonResponse({
                'status': 404,
                'type': 'error',
                'message': "Erreur de modification", 
                'redirectLink': {
                    'link': link,
                },
            })

    form = SiteInfoForm(instance=site, use_required_attribute=False)
    return render(request, 'dashboard/site_edit.html', {'site': site, 'form': form})

def site_delete(request):
    pass


# API call for get relances data
class ListRelances(APIView):
    """
    View to list all relances in the system.

    * Requires session authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all relances.
        """
        relances = get_site_relance(request)
        labels = []
        contents = []
        data = {}
        months = get_year_month()
        cc = dict()
        info = {}
        
        for relance in relances:
            
            owner = relance['owner']
            for month in months:
                relance_date_str = relance['relance_date'].strftime("%B")
                if relance_date_str == month[1]:
                    if info.get(month[1]):
                        info[month[1]] += 1
                    else:
                        info.setdefault(month[1], 1)
            if cc.get(owner):
                cc[owner] += 1
            else:
                cc.setdefault(owner, 1)

        for month in months:
            labels.append(month[1])
            if month[1] in info:
                contents.append(info[month[1]])
            else:
                contents.append(0)

        data = {
            'labels': labels,
            'contents': contents,
            'type': 'success',
        }

        return Response(data, status=200)


def handle_404(request):
    return render(request, '404.html')

def handle_403(request):
    return render(request, '403.html')

def handle_500(request):
    return render(request, '500.html')