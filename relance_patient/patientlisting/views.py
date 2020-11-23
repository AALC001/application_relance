import asyncio
import calendar
import random
from time import strftime
from django.http.response import HttpResponse
from numpy.core.getlimits import finfo
import pandas as pd
import numpy as np
import datetime as dt
import tempfile
import math
import locale
import dateutil
import activite_relance as ar
import dashboard.models as dash_mod
import json
# from pandas.io import json
from operator import attrgetter
from secrets import token_hex
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from datetime import datetime
from .models import PatientListing
from .extractxlsx import PatientExtractXLSX
from openpyxl.utils import get_column_letter, column_index_from_string
from  django.conf import settings
from dashboard.models import SiteInfo
from relance_patient.utils import download as file_download, converter
from pandas import DataFrame
from asgiref.sync import sync_to_async
from activite_relance.models import Patient, DateRDV, Venue, PersonSoutien
from relance_patient.utils import get_month_limit, get_year_month, get_list_year
from django.views import View
from relance_patient.utils import export_to_pdf
from django.core.paginator import Paginator
from django.db import connections


def generate_filename():
    now_date = datetime.now().date()
    now_time = datetime.now().time()
    return str(now_date).replace('-', '') + str(now_time).split('.')[0].replace(':', '')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))


def check_if_patient_exist(code_patient):
    return ar.models.Patient.objects.filter(code_patient=code_patient).exists()

def save_patient_data(patients:list, rdv_date:list, persones_soutiens: list, site: dash_mod.SiteInfo):
    result = []
    for x, y, z in zip(patients, rdv_date, persones_soutiens):
        patient_data = {"site":site, "first_name":x['Nom_Patient'], "last_name":x['Prenoms_Patient'], "sexe":x['Sexe'], "age":x['Age'], "situation_matrimoniale":x['Situation_matrimoniale'], "contact":x['Contact_Téléphonique'], "domicile":x['Lieu_Habitation']}

        rdv_data = { "date_last_arv":y['Date_dernier_ARV'], "date_proch_arv":y['Date_prochain_ARV'],"date_last_cv":y['Date_Dernier_CV'],"date_proch_cv":y['Date_prochain_CV']}

        person_soutient_data = {"first_name":z['Nom_Personne_Soutien'], "last_name":z['Prénoms_Personne_Soutien'], "adresse":z['Adresse_Personne_Soutien'], "contact":z['Contact_Personne_Soutien'], "lien":z['Lien_Patient']}

        patient, patient_created = ar.models.Patient.objects.update_or_create(code_patient=x['Code_Patient'], defaults = patient_data)
        rdv, rdv_created = ar.models.DateRDV.objects.update_or_create(patient=patient, defaults=rdv_data)
        person, person_created = ar.models.PersonSoutien.objects.update_or_create(patient=patient, defaults=person_soutient_data)

        # try:
        #     patient = ar.models.Patient.objects.get(code_patient=x['Code_Patient'])
        #     rdv = ar.models.DateRDV.objects.get(patient=patient)
        #     person = ar.models.PersonSoutien.objects.get(patient=patient)

        #     for k, v in patient_data.items():
        #         setattr(patient, k, v)
        #     patient.save()

        #     for k, v in date_data.items():
        #         setattr(rdv, k, v)
        #     rdv.save()

        #     for k, v in person_soutient_data.items():
        #         setattr(person, k, v)
        #     person.save()

        # except ar.models.Patient.DoesNotExist:

        #     patient = ar.models.Patient(site=site , code_patient=x['Code_Patient'], first_name=x['Nom_Patient'], last_name=x['Prenoms_Patient'], sexe=x['Sexe'], age=x['Age'], situation_matrimoniale=x['Situation_matrimoniale'], contact=x['Contact_Téléphonique'], domicile=x['Lieu_Habitation'])
        #     patient.save()

        #     rdv = ar.models.DateRDV(
        #         patient=patient, 
        #         date_last_arv=y['Date_dernier_ARV'], 
        #         date_proch_arv=y['Date_prochain_ARV'],
        #         date_last_cv=y['Date_Dernier_CV'],
        #         date_proch_cv=y['Date_prochain_CV'],)
        #     rdv.save()

        #     person = ar.models.PersonSoutien(patient=patient, first_name=z['Nom_Personne_Soutien'], last_name=z['Prénoms_Personne_Soutien'], adresse=z['Adresse_Personne_Soutien'], contact=z['Contact_Personne_Soutien'], lien=z['Lien_Patient'])
        #     person.save()

        if patient_created and rdv_created and person_created:
            result.append(True)
        else:
            result.append(False)

    return all(result)

# Patient listing home
def index(request):
    return render(request, "patientlisting/index.html")

def extract_patient_data(filename, file_type="xlsx", header=1):
    df = None
    if file_type == "xlsx":
        df = pd.read_excel(filename, header=header)
    
    df_patient = df.loc[:,'Code_Patient':'Contact_Téléphonique']
    df_dateRDV = df.loc[:,'Date_Dernier_CV':'Date_prochain_ARV']
    df_person_soutient = df.loc[:,'Nom_Personne_Soutien':'Lien_Patient']

    patient_list = []
    date_RDV_list = []
    person_soutien_list = []

    for i, row in df_patient.iterrows():
        patient_list.append(row.to_dict())

    for i, row in df_dateRDV.iterrows():
        date_RDV_list.append(row.to_dict())

    for i, row in df_person_soutient.iterrows():
        person_soutien_list.append(row.to_dict())

    return [patient_list, date_RDV_list, person_soutien_list,]


def upload_patient_file(request):
    site = SiteInfo.objects.filter(site_code=request.user.user.site_code).first()
    if request.method == "POST":
        patient_file = request.FILES['patient_file']
        fs = FileSystemStorage()
        file_path = Path(patient_file.name)
        new_file_name = f'{token_hex(8)}{generate_filename()}{file_path.suffix}'
        filename = fs.save(new_file_name, patient_file)
        url = fs.url(filename)
        
        if site:
            site.patient_file = url
            site.save()

            patient_list, dateDRV_list, person_soutien_list = extract_patient_data(url)

            result = sync_to_async(save_patient_data(patient_list, dateDRV_list, person_soutien_list, site), thread_sensitive=True)

            if result:
                return JsonResponse({'type': 'success', 'message': 'Enregistrement des patients réussie'})
            else:
                return JsonResponse({'type': 'error', 'message': 'Erreur d\'enregistrement des patients'})
        else:
            return JsonResponse({'type': 'error', 'message': 'Erreur d\'enregistrement des patients'})

    patients = ar.models.Patient.objects.filter(site=site)
    context = {
        'patients': patients
    }
    return render(request, "patientlisting/upload_patient.html", context)


# Download patient fiche modele file
def download_patient_model_file(request):
    filename = "documents/modele_fiche_patient.xlsx"
    download = file_download(request, filename)
    return download

# Download site last upload file
def download_patient_uploaded_file(request):
    filename = request.user._get_account_site.patient_file
    download = file_download(request, filename, is_uploaded=True)
    return download

#save file content to db
def save_file_content(request):
    if request.method == "POST":
        patient_listing = PatientListing.objects.filter(account=request.user)


#RDV list month
# def month_RDV(request):
#     dates = DateRDV.objects.all()
#     list_of_month = get_year_month()
#     years = get_list_year(2000, 2099)
#     now = dt.date.today()
#     patient_rdv = []
#     arv_rdv = []
#     cv_rdv = []
#     filtred_RDV = []
#
#     if request.GET.get('listing_month') or request.GET.get('listing_year'):
#         month = int(request.GET['listing_month']) or now.month
#         year = int(request.GET['listing_year'])  or now.year
#         start_date, end_date = get_month_limit(year, month)
#
#         for date in dates:
#             if start_date <= date.date_proch_arv <= end_date and date.date_proch_arv >= now:
#                 data = {}
#                 data['patient'] = date.patient
#                 data['date_rdv'] = json.dumps(date.date_proch_arv, default=str)
#                 data['rdv_type'] = "arv"
#                 arv_rdv.append(data)
#
#             if start_date <= date.date_proch_cv <= end_date and date.date_proch_cv >= now :
#                 data = {}
#                 data['patient'] = date.patient
#                 data['date_rdv'] = json.dumps(date.date_proch_cv, default=str)
#                 data['rdv_type'] = "cv"
#                 cv_rdv.append(data)
#
#         patient_rdv = arv_rdv + cv_rdv
#         filtred_RDV = sorted(patient_rdv, key=lambda x: x['date_rdv'])
#         serialize_data = filtred_RDV
#
#         rdv_month = {
#             'type': 'rdv_month',
#             'period': {
#                 'month': str(month),
#                 'year': str(year),
#             },
#             'data': json.dumps(serialize_data, default=converter)
#         }
#
#         request.session['rdv_month_listing'] = rdv_month
#
#     for item in filtred_RDV:
#         item['date_rdv'] = dt.datetime.strptime(json.loads(item['date_rdv']), "%Y-%m-%d").date()
#
#     context = {'list_of_month': list_of_month, 'patient_rdv': filtred_RDV, 'years': years, 'cur_year': now.year}
#     return render(request, "patientlisting/listing/month_rdv.html", context)

# version 2
def month_RDV(request):
    list_of_month = get_year_month()
    years = get_list_year(2000, 2099)
    now = dt.date.today()
    patient_rdv = []

    if request.session.get('rdv_month_listing'):
        patient_rdv = json.loads(request.session['rdv_month_listing']['data'])

        for item in patient_rdv:
            item['date_rdv'] = dt.datetime.strptime(item['date_rdv'].split('/')[0], '%Y-%m-%d').date()

    filtred_RDV = sorted(patient_rdv, key=lambda x: x['date_rdv'])

    paginator = Paginator(filtred_RDV, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'list_of_month': list_of_month, 'page_obj': page_obj, 'years': years, 'cur_year': now.year}
    return render(request, "patientlisting/listing/month_rdv.html", context)

def missed_RDV(request):
    list_of_month = get_year_month()
    years = get_list_year(2000, 2099)
    type_concept = (5096, 165040)
    now = dt.date.today()
    period = ''
    missed_RDV = []
    missed_limit = 28

    if request.GET.get('listing_month') or request.GET.get('listing_year'):
        month = int(request.GET['listing_month']) or now.month
        year = int(request.GET['listing_year'])  or now.year
        period = str([k for k in get_year_month() if k[0] == month][0][1]) + " " + str(year)
        start_date, end_date = get_month_limit(year, month)
            
        with connections['sigdep'].cursor() as cursor:
            query = '''
            SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
            FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
            WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id in %s and ob.value_datetime BETWEEN %s and %s and DATEDIFF(ob.value_datetime, NOW())<0 and ABS(DATEDIFF(ob.value_datetime, NOW()))<%s
            ORDER BY ob.value_datetime desc'''

            cursor.execute(query, (type_concept, start_date, end_date, missed_limit))
            row = list(dictfetchall(cursor))

        missed_RDV = sorted(row, key=lambda x: x['date_rdv'])
        serialize_data = missed_RDV


        rdv_missed = {
            'type': 'rdv_missed',
            'period': period,
            'data': json.dumps(serialize_data, default=converter)
        }

        request.session['rdv_missed_listing'] = rdv_missed

    paginator = Paginator(missed_RDV, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'years': years, 'cur_year': now.year, 'list_of_month': list_of_month, }

    return render(request, 'patientlisting/listing/missed_rdv.html', context)


# Missed RDV
# def missed_RDV(request):
#     dates = DateRDV.objects.all()
#     list_of_month = get_year_month()
#     years = get_list_year(2000, 2099)
#     now = dt.date.today()
#     arv_rdv = []
#     cv_rdv = []
#     missed_RDV = []
#     missed_limit = 28
#
#     if request.GET.get('listing_month') or request.GET.get('listing_year'):
#         month = int(request.GET['listing_month']) or now.month
#         year = int(request.GET['listing_year'])  or now.year
#         start_date, end_date = get_month_limit(year, month)
#
#         for date in dates:
#             tdelta_arv = (date.date_proch_arv - now).days
#             tdelta_cv = (date.date_proch_cv - now).days
#
#             if start_date <= date.date_proch_arv <= end_date and tdelta_arv < 0 and abs(tdelta_arv) < missed_limit:
#             # if tdelta_arv < 0 and abs(tdelta_arv) < missed_limit:
#                 data = {}
#                 data['patient'] = date.patient
#                 data['date_rdv'] = json.dumps(date.date_proch_arv, default=str)
#                 data['rdv_type'] = "arv"
#                 arv_rdv.append(data)
#
#             if start_date <= date.date_proch_cv <= end_date and tdelta_cv < 0 and tdelta_cv < missed_limit:
#             # if tdelta_cv < 0 and tdelta_cv < missed_limit:
#                 data = {}
#                 data['patient'] = date.patient
#                 data['date_rdv'] = json.dumps(date.date_proch_cv, default=str)
#                 data['rdv_type'] = "cv"
#                 cv_rdv.append(data)
#
#         patient_rdv = arv_rdv + cv_rdv
#         missed_RDV = sorted(patient_rdv, key=lambda x: x['date_rdv'])
#         serialize_data = missed_RDV
#
#         rdv_missed = {
#             'type': 'rdv_month',
#             'period': {
#                 'month': str(month),
#                 'year': str(year),
#             },
#             'data': json.dumps(serialize_data, default=converter)
#         }
#
#         request.session['rdv_missed_listing'] = rdv_missed
#
#     for item in missed_RDV:
#         item['date_rdv'] = dt.datetime.strptime(json.loads(item['date_rdv']), "%Y-%m-%d").date()
#
#     context = {'missed_rdv': missed_RDV, 'years': years, 'cur_year': now.year, 'list_of_month': list_of_month, }
#
#     return render(request, 'patientlisting/listing/missed_rdv.html', context)

# version 2
def list_PVD(request):
    now = dt.date.today()
    type_lost_patient = [28, 90]
    losted_RDV = []
    type_concept = (5096, 165040)

    if request.GET.get('type_losted'):
        limit = int(request.GET.get('type_losted'))

        with connections['sigdep'].cursor() as cursor:

            if limit == 28:

                query = '''
                SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
                FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
                WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id in %s and DATEDIFF(NOW(), ob.value_datetime)>=28 and DATEDIFF(NOW(), ob.value_datetime)<= 90
                ORDER BY ob.value_datetime desc'''
            elif limit == 90:
                query = '''
                SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
                FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
                WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id in %s and DATEDIFF(NOW(), ob.value_datetime)>=90
                ORDER BY ob.value_datetime desc'''

            cursor.execute(query, (type_concept, ))
            row = list(dictfetchall(cursor))

        losted_RDV = sorted(row, key=lambda x: x['date_rdv'])
        serialize_data = losted_RDV

        rdv_losted = {
            'type': limit,
            'data': json.dumps(serialize_data, default=converter)
        }

        request.session['patient_lost_listing'] = rdv_losted

    paginator = Paginator(losted_RDV, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'type_lost_patient': type_lost_patient, 'page_obj': page_obj}
    return render(request, 'patientlisting/listing/lost_patient.html', context)

#patient lost
# def list_PVD(request):
#     # dates = DateRDV.objects.all()
#     now = dt.date.today()
#     type_lost_patient = [28, 90]
#     losted_arv = []
#     losted_cv = []
#     losted_RDV = []
#     query = ''
#
#     if request.GET.get('type_losted'):
#         limit = int(request.GET.get('type_losted'))
#
#         with connections['sigdep'].cursor() as cursor:
#
#             if limit == 28:
#                 query = '''
#                 SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
#                 FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
#                 WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=5096 and ob.value_datetime BETWEEN %s and %s
#                 ORDER BY ob.value_datetime desc'''
#
#             elif limit == 90:
#                 query = '''
#                 SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
#                 FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
#                 WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=5096 and ob.value_datetime BETWEEN %s and %s
#                 ORDER BY ob.value_datetime desc'''
#
#             row = list(dictfetchall(cursor))
#
#             for date in dates:
#                 tdelta_arv = (date.date_proch_arv - now).days
#                 tdelta_cv = (date.date_proch_cv - now).days
#                 if tdelta_arv < 0 and limit <= abs(tdelta_arv) < 90:
#                     data = {}
#                     data['patient'] = date.patient
#                     data['date_rdv'] = json.dumps(date.date_proch_arv, default=str)
#                     data['rdv_type'] = "arv"
#                     losted_arv.append(data)
#
#                 if tdelta_cv < 0  and limit <= abs(tdelta_cv) < 90:
#                     data = {}
#                     data['patient'] = date.patient
#                     data['date_rdv'] = json.dumps(date.date_proch_arv, default=str)
#                     data['rdv_type'] = "cv"
#                     losted_cv.append(data)
#
#             losted_RDV = losted_arv + losted_cv
#
#         elif limit == 90:
#             for date in dates:
#                 tdelta_arv = (date.date_proch_arv - now).days
#                 tdelta_cv = (date.date_proch_cv - now).days
#
#                 if tdelta_arv < 0 and abs(tdelta_arv) >= 90 :
#                     data = {}
#                     data['patient'] = date.patient
#                     data['date_rdv'] = json.dumps(date.date_proch_arv, default=str)
#                     data['rdv_type'] = "arv"
#                     losted_arv.append(data)
#
#                 if tdelta_cv < 0 and abs(tdelta_cv) >= 90 :
#                     data = {}
#                     data['patient'] = date.patient
#                     data['date_rdv'] = json.dumps(date.date_proch_arv, default=str)
#                     data['rdv_type'] = "cv"
#                     losted_cv.append(data)
#
#             # losted_RDV = losted_arv + losted_cv
#
#     serialize_data = losted_RDV
#
#     rdv_losted = {
#         'type': 'rdv_month',
#         'data': json.dumps(serialize_data, default=converter)
#     }
#
#
#     for item in losted_RDV:
#         item['date_rdv'] = dt.datetime.strptime(json.loads(item['date_rdv']), "%Y-%m-%d").date()
#
#
#     request.session['patient_lost_listing'] = rdv_losted
#     context = {'type_lost_patient': type_lost_patient, 'losted_RDV': losted_RDV}
#     return render(request, 'patientlisting/listing/lost_patient.html', context)


# GENERATE MONTH RDV LIST
class GenerateMonthRDVListingPDF(View):
    def get(self, request, *args, **kwargs):

        # Set locale time to french
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        # Template for the view
        template_src = 'reports/month_rdv_listing.html'

        period = request.session['rdv_month_listing']['period']

        # load moth rdv in the session
        session_data = json.loads(request.session['rdv_month_listing']['data'])

        # For each rdv object convert dupms date to datetime object
        for item in session_data:
            # item['date_rdv'] = dt.datetime.strptime(item['date_rdv'], "%Y-%m-%d").date()
            item['date_rdv'] = dt.datetime.strptime(item['date_rdv'].split('/')[0], '%Y-%m-%d').date()



        # define conext
        context = {
            'rdv_month_listing': session_data,
            'user': request.user,
            'service': request.user._get_account_site,
            'period': period,
            'type_rdv': request.session['rdv_month_listing']['type'],
        }

        # response headers
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=LISTING_RDV_"+ period.upper() +'.pdf'
        response['Content-Transfer-Encoding'] = "binary"

        # Create pdf file using export_to_pdf func
        result = export_to_pdf(template_src, context)

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response


# GENERATE MONTH MISSED RDV LIST
class GenerateMissedRDVListingPDF(View):
    def get(self, request, *args, **kwargs):

        # Set locale time to french
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        # Template for the view
        template_src = 'reports/missed_rdv_listing.html'

        # get period of rdv from session
        # period = str(request.session['rdv_missed_listing']['period']['month']) + '-' + request.session['rdv_missed_listing']['period']['year']
        period = request.session['rdv_missed_listing']['period']
        # period_str = dt.datetime.strptime(period, '%m-%Y').strftime('%B %Y')

        # load moth rdv in the session
        session_data = json.loads(request.session['rdv_missed_listing']['data'])

        # For each rdv object convert dupms date to datetime object
        for item in session_data:
            # item['date_rdv'] = dt.datetime.strptime(json.loads(item['date_rdv']), "%Y-%m-%d").date()
            item['date_rdv'] = dt.datetime.strptime(item['date_rdv'].split('/')[0], '%Y-%m-%d').date()

        # define conext
        context = {
            'rdv_missed_listing': session_data,
            'user': request.user,
            'service': request.user._get_account_site,
            'period': period,
        }

        # response headers
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=LISTING_MISSED_RDV_"+ period.upper() +'.pdf'
        response['Content-Transfer-Encoding'] = "binary"

        # Create pdf file using export_to_pdf func
        result = export_to_pdf(template_src, context)

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response


# GENERATE MONTH MISSED RDV LIST
class GenerateLostPatientListingPDF(View):
    def get(self, request, *args, **kwargs):

        # Set locale time to french
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        # Template for the view
        template_src = 'reports/lost_patient_listing.html'

        # load moth rdv in the session
        session_data = json.loads(request.session['patient_lost_listing']['data'])
        type_losted = request.session['patient_lost_listing']['type']

        # For each rdv object convert dupms date to datetime object
        for item in session_data:
            # item['date_rdv'] = dt.datetime.strptime(json.loads(item['date_rdv']), "%Y-%m-%d").date()
            item['date_rdv'] = dt.datetime.strptime(item['date_rdv'].split('/')[0], '%Y-%m-%d').date()

        # define conext
        context = {
            'rdv_lost_listing': session_data,
            'user': request.user,
            'service': request.user._get_account_site,
            'type_losted': type_losted
        }

        # response headers
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=LISTING_LOST_RDV_" + dt.date.today().strftime("%d-%m-%Y").upper() +'.pdf'
        response['Content-Transfer-Encoding'] = "binary"

        # Create pdf file using export_to_pdf func
        result = export_to_pdf(template_src, context)

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response