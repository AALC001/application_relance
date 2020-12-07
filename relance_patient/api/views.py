
import json
import locale

from datetime import datetime
from django.shortcuts import render
from django.db import connections
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from relance_patient.utils import date_in_month, date_in_year, get_month_limit, converter, get_year_month

#
# # Get ARV or Clinic RDV
# def get_arv_or_clinic(rdv_list, listing_type, rdv_code):
#     if listing_type['type'] == 'month':
#         month = listing_type['listingMonth']
#         year = listing_type['listingYear']
#
#         if month != None or year != None:
#             print(month, year)
#             return [rdv for rdv in rdv_list if rdv['reason'] == rdv_code and date_in_year(rdv['date_rdv'], year) and date_in_month(rdv['date_rdv'], month)]
#
#     elif listing_type == 'interval':
#         start = listing_type['listingStartDate']
#         end = listing_type['listingEndDate']
#
#         if start != None or end != None:
#             print(start, end)
#             return [rdv for rdv in rdv_list if rdv['reason'] == rdv_code and start <= rdv['date_rdv'] <= end]
#
#
# # Get patient RDV by type
# def getPatientRDV(rdv_list:list, rdv_type:str, rdv_filter:str) -> list:
#     listing_filter = json.loads(rdv_filter)
#     print(listing_filter)
#
#     if rdv_type == 'rdv_arv':
#         return get_arv_or_clinic(rdv_list, listing_filter, 165040)
#     return get_arv_or_clinic(rdv_list, listing_filter, 5096)




# Get data from db on dict type
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))


class ListRDV(APIView):
    """
        List all obs
    """
    def get(self, request, format=None):
        locale.setlocale(locale.LC_TIME, locale='fr_FR.UTF-8')
        params = request.query_params
        type_listing = json.loads(params['listingType'], encoding='utf-8')
        type_rdv = params['rdvType']
        period = ''

        with connections['sigdep'].cursor() as cursor:
            # query = ''
            if type_rdv == 'arv':
                if type_listing['type'] == 'interval':
                    query = """
                    SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
                    FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
                    WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=5096 and ob.value_datetime BETWEEN %s and %s
                    ORDER BY ob.value_datetime desc"""
                elif type_listing['type'] == 'month':
                    query = """
                    SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
                    FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
                    WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=5096 and MONTH(ob.value_datetime)=%s and YEAR(ob.value_datetime)=%s
                    ORDER BY ob.value_datetime desc"""

            elif type_rdv == 'clinic':
                if type_listing['type'] == 'interval':
                    query = """
                    SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
                    FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
                    WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=165040 and ob.value_datetime BETWEEN %s and %s
                    ORDER BY ob.value_datetime desc"""
                elif type_listing['type'] == 'month':
                    query = """
                    SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
                    FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
                    WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=165040 and MONTH(ob.value_datetime)=%s and YEAR(ob.value_datetime)=%s
                    ORDER BY ob.value_datetime desc"""
# #have to change concept id value

#             elif type_rdv == 'virale':
#                 if type_listing['type'] == 'interval':
#                     query = """
#                     SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
#                     FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
#                     WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=165040 and ob.value_datetime BETWEEN %s and %s
#                     ORDER BY ob.value_datetime desc"""
#                 elif type_listing['type'] == 'month':
#                     query = """
#                     SELECT pi.identifier as patient_code, pn.family_name as first_name, pn.given_name as last_name, per.gender, per.birthdate, ob.value_datetime as date_rdv, ob.concept_id as reason
#                     FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
#                     WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id and ob.concept_id=165040 and MONTH(ob.value_datetime)=%s and YEAR(ob.value_datetime)=%s
#                     ORDER BY ob.value_datetime desc"""

            if type_listing['type'] == 'interval':
                start_date = datetime.strptime(type_listing['listingStartDate'], '%Y-%m-%d').date()
                end_date = datetime.strptime(type_listing['listingEndDate'], '%Y-%m-%d').date()

                if start_date > end_date:
                    cursor.execute(query, (end_date, start_date))
                    period = type_listing['listingEndDate'] + " " + type_listing['listingStartDate']
                else:
                    cursor.execute(query, (start_date, end_date))
                    period = type_listing['listingStartDate'] + " " + type_listing['listingEndDate']

            elif type_listing['type'] == 'month':
                month = int(type_listing['listingMonth'])
                year = int(type_listing['listingYear'])
                period = str([k for k in get_year_month() if k[0] == month][0][1]) + " " + str(year)
                cursor.execute(query, (month, year))

            row = list(dictfetchall(cursor))
        filtred_RDV = sorted(row, key=lambda x: x['date_rdv'])
        serialize_data = filtred_RDV


        patient_expected = {
            'type': type_rdv,
            'period': period,
            'reset': False,
            'data': json.dumps(serialize_data, default=converter)
        }

        request.session['rdv_month_listing'] = patient_expected

        return Response({'type': 'success', 'msg': 'génération de listing éffectué'}, status=200)

def count_patient(request):
    query='''SELECT per.person_id
    FROM person as per, obs as ob, person_name as pn, patient_identifier as pi
    WHERE per.person_id=ob.person_id and pn.person_id=per.person_id and per.person_id=pi.patient_id
    ORDER BY ob.value_datetime desc'''

    with connections['sigdep'].cursor() as cursor:
        cursor.execute(query)
        row = list(dictfetchall(cursor))
    
    count = len(row)
    return JsonResponse({
        'type': 'success', 
        'status': 200, 
        'data': {'count': count}
        })