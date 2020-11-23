import json
import secrets
import datetime
import tempfile
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.template.loader import get_template, render_to_string
from .models import FicheRelance
from relance_patient.utils import export_to_pdf



def load_relance_list(relances:str) -> list:
    return json.loads(relances)

def get_not_archive_relance(relances:list) -> list:
    return [ relance for relance in relances if not relance['is_archive']]

def get_archive_relance(relances:list) -> list:
    return [ relance for relance in relances if relance['is_archive']]

def get_filtred_relances(relances, *args, **kwargs):
    feedback = kwargs['feedback']
    start = kwargs['start_date']
    end = kwargs['end_date']
    results = []

    if feedback and start and end:
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if relance['feedback']['type'].lower() == feedback.lower() and start <= cur <= end:
                results.append(relance)
        return {'relances': results, 'period': {'start': start.strftime('%m/%d/%Y'), 'end': end.strftime('%m/%d/%Y')}}

    if feedback and start and not end:
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if relance['feedback']['type'].lower() == feedback.lower() and start <= cur:
                results.append(relance)
        return {'relances': results, 'period': {'start': start.strftime('%m/%d/%Y'), 'end': ''}}

    if feedback and not start and end:
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if relance['feedback']['type'].lower() == feedback.lower() and cur <= end:
                results.append(relance)
        return {'relances': results, 'period': {'start': '', 'end': end.strftime('%m/%d/%Y')}}

    if not feedback and start and end:
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if start <= cur <= end:
                results.append(relance)
        return {'relances': results, 'period': {'start': start.strftime('%m/%d/%Y'), 'end': end.strftime('%m/%d/%Y')}}
    
    if not feedback and start and not end:
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if start <= cur:
                results.append(relance)
        return {'relances': results, 'period': {'start': start.strftime('%m/%d/%Y'), 'end': ''}}

    if not feedback and not start and end:
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if cur <= end:
                results.append(relance)
        return {'relances': results, 'period': {'start': '', 'end': end.strftime('%m/%d/%Y') }}

    if feedback and not start and not end:
        for relance in relances:
            cur = datetime.datetime.strptime(relance['relance_date'], "%Y-%m-%d").date()
            if relance['feedback']['type'].lower() == feedback.lower():
                results.append(relance)
        return {'relances': results, 'period': {'start': '', 'end': ''}}

    return {'relances': relances, 'period': {'start': '', 'end': ''}}


# Liste all cc relance for site admin
def list_site_relance(request):
    fiche_relance = FicheRelance.objects.all();
    site_user_relance = []
    relances = []
    # filtred_relances = {}
    filtred_relances = {'relances': [], 'period': {'start': '', 'end': ''}}
    info = {}


    for fiche in fiche_relance:
        if fiche.account.user.site_code == request.user.user.site_code:
            site_user_relance.append(fiche)
   
    if site_user_relance:
        for site_fiche in site_user_relance:
            relance_user = site_fiche.account

            for relance in load_relance_list(site_fiche.info_relance):
                relance['owner'] = f"{relance_user.user.first_name} {relance_user.user.last_name}"
                relances.append(relance)

    feedback = request.GET.get('relance_feedback')
    relance_start_at = request.GET.get('relance_start_at')
    relance_end_at = request.GET.get('relance_end_at')

    filtred_relances['relances'] = relances
    request.session['relances'] = filtred_relances['relances']
    request.session['relances_periode'] = filtred_relances['period']

    if 'relance_feedback' in request.GET or 'relance_start_at' in request.GET or 'relance_end_at' in request.GET:
        feedback = request.GET['relance_feedback']
        relance_start_at = request.GET.get('relance_start_at')
        relance_end_at = request.GET.get('relance_end_at')

        results = get_filtred_relances(relances, feedback=feedback, start_date=relance_start_at, end_date=relance_end_at)
        filtred_relances['relances'] = results['relances']
        filtred_relances['period'] = results['period']

        # filtred_relances['relances'] = relances
        # filtred_relances['period'] = {'start': 'start date', 'end': 'end date'}

        request.session['relances'] = filtred_relances['relances']
        request.session['relances_periode'] = filtred_relances['period']

    context = {'relances': filtred_relances['relances']}

    return render(request, 'relance_patient/all_relance.html', context)

#affice toute les relances faites par l'utilisateur
def list_relance(request):
    fiche_relance = FicheRelance.objects.filter(account=request.user).first()
    relances = []

    if fiche_relance:
        relances = get_not_archive_relance(json.loads(fiche_relance.info_relance))
        
    
    context = {'relances': relances}
    return render(request, 'relance_patient/index.html', context)

#Ajouter une relance
def add_relance(request):
    if request.method == "POST":
        form_data = request.POST
        relance_reason = form_data['relance_reason']
        if relance_reason == 'other':
            relance_reason = form_data['relance_reason_other']
        infos_relance = {
            'relance_code': secrets.token_hex(8),
            'relance_date': form_data['relance_date'],
            'patient_code': form_data['patient_code'],
            'patient_contact': form_data['patient_contact'],
            'relance_reason': relance_reason,
            'type_relance': {
                'type': form_data['relance_type'],
                'relance_call_duration': form_data['call_durantion']
            },
            'feedback': {
                'type': form_data['relance_feedback'],       
                'visite_date': form_data['feedback_visite_date'],         
            },
            'comment': form_data['relance_comment'],
            'is_archive': False,
        }

        account_relance = FicheRelance.objects.filter(account=request.user).first()
        account_relance_infos_relance = []

        if account_relance:
            account_relance_infos_relance = json.loads(account_relance.info_relance, encoding="utf-8")
            account_relance_infos_relance.append(infos_relance)
            account_relance.info_relance = json.dumps(account_relance_infos_relance)
            account_relance.save()
        else:
            account_relance_infos_relance.append(infos_relance)
            FicheRelance.objects.create(account=request.user, info_relance=json.dumps(account_relance_infos_relance))

        
        link = reverse('activite_relance:list_relance')

        return JsonResponse({
            'status': 200,
            'type': 'success',
            'message': "La relance a été ajoutée", 
            'redirectLink': {
                'link': link,
            }, 
        })


    motifs = ['index testing', 'arv', 'prélèvement cv', 'suivi clinique', 'resultat cv', 'education thérapeutique', 'bilan initial',]
    feedback = ['auto transféré', 'transféré', 'injoignable', 'décédé', 'réfus', 'recherche en cours', 'arrêt volontaire', 'retour aux soins', 'promesse de retour']

    feedback.sort()
    motifs.sort()

    context = {'motifs': motifs, 'feedback': feedback}
    return render(request, "relance_patient/add.html", context)

#Supprimer une relance
def remove_relance(request):
    pass

#Modifier une relance
def edit_relance(request, relance_code):
    fiche_relance = FicheRelance.objects.filter(account=request.user).first()
    relances = load_relance_list(fiche_relance.info_relance)
    cur_relance = None

    if request.method == "POST":
        data = request.POST
        relance_code = data['relance_code']
        relance_reason = data['relance_reason']

        if relance_reason == 'other':
            relance_reason = data['relance_reason_other']

        for relance in relances:
            if relance['relance_code'] == relance_code:
                relance['patient_code'] = data['patient_code']
                relance['patient_contact'] = data['patient_contact']
                relance['relance_date'] = data['relance_date']
                relance['relance_reason'] = relance_reason
                relance['type_relance']['type'] = data['relance_type']
                relance['type_relance']['relance_call_duration'] = data['call_durantion']
                relance['feedback']['type'] = data['relance_feedback']
                relance['comment'] = data['relance_comment']

                if relance['feedback']['type'].lower() != "promesse de retour":
                    relance['feedback']['visite_date'] = ""
                else:
                    relance['feedback']['visite_date'] = data['feedback_visite_date']

        fiche_relance.info_relance = json.dumps(relances)
        fiche_relance.save()

        link = reverse('activite_relance:list_relance')
        return JsonResponse({
            'status': 200,
            'type': 'success',
            'message': "La relance a été modifiée", 
            'redirectLink': {
                'link': link,
            }, 
        })

    
    for relance in relances:
        if relance['relance_code'] == relance_code:
            cur_relance = relance
            break
    
    motifs = ['index testing', 'arv', 'prélèvement cv', 'suivi clinique', 'resultat cv', 'education thérapeutique', 'bilan initial',]

    feedback = ['auto transféré', 'transféré', 'injoignable', 'décédé', 'réfus', 'recherche en cours', 'arrêt volontaire', 'retour aux soins', 'promesse de retour']

    feedback.sort()
    motifs.sort()
    context = {'relance': cur_relance, 'motifs': motifs, 'feedback': feedback}
    return render(request, "relance_patient/edit.html", context)


def archive_relance(request, relance_code):
    data = request.POST
    fiche_relance = FicheRelance.objects.filter(account=request.user).first()
    relances = load_relance_list(fiche_relance.info_relance)

    for relance in relances:
        if relance['relance_code'] == data['relance_code']:
            relance['is_archive'] = True

    fiche_relance.info_relance = json.dumps(relances)
    fiche_relance.save()

    return JsonResponse({
        'status': 200,
        'type': 'success',
        'message': "La relance a été archivée", 
    })

# Generate relance report (ext: PDF)
class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template_src = 'reports/fiche_relance_report.html'
        context = {
            'relances': request.session.get('relances', []),
            'relances_periode': request.session.get('relances_periode'),
            'user': request.user,
            'service': request.user._get_account_site
        }
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=Relance_Patient" + str(datetime.datetime.now()) + '.pdf'
        response['Content-Transfer-Encoding'] = "binary"

        result = export_to_pdf(template_src, context)
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response