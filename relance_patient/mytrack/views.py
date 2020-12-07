import json
import secrets
import datetime as dt
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from .models import Respect, FicheIndex, FicheRdv
from django.db import connections
# Create your views here. 

def load_info(info:str) -> list:
    return json.loads(info)

def get_not_archive_info(info:str) -> list:
    return [data for data in info if not data['is_archive']]

def get_archive_info(info) -> list:
    return [data for data in info if data['is_archive']]


def list_is_come(request):
    venue = Respect.objects.filter(account=request.user).first()
    come = []
    if venue:
        come = get_not_archive_info(json.loads(venue.info_respect_rdv))
        
    context = {'come': come}
    return render(request, 'mytrack/respect_temps/list_venue.html', context)


def respect_rdv(request):
    if request.method=='POST':
        form_data = request.POST
        info_respect = {
            'code_respect':secrets.token_hex(8),
            'date':form_data['relance_date'],
            'code_patient':form_data['patient_code'],
            'reason':', '.join(form_data.getlist('motif')),
            'comment':form_data['respect_comment'],
            'is_archive': False,
        }
        respect = Respect.objects.filter(account=request.user).first()
        if respect:
            respect_values = json.loads(respect.info_respect_rdv, encoding="utf-8")
            respect_values.append(info_respect)
            respect.info_respect_rdv = json.dumps(respect_values)
            respect.save()
        else:
            respect_values = []
            respect_values.append(info_respect)
            Respect.objects.create(account=request.user,info_respect_rdv=json.dumps(respect_values))
        
        rdv = FicheRdv.objects.filter(account=request.user).first()
        list_rdv = json.loads(rdv.info_rdv)
        for i in list_rdv:
            if dt.datetime.strptime(info_respect["date"],'%Y-%m-%d').date()<=dt.datetime.strptime(i["date_rdv"],'%Y-%m-%d').date() and info_respect["code_patient"]==i["patient_code"] and info_respect["reason"]==i["motif"] and i["is_archive"]==False:
                i["is_archive"]=True
                list_rdv[list_rdv.index(i)]=i
        rdv.info_rdv=json.dumps(list_rdv)
        rdv.save()
        print(rdv.info_rdv)

        link = reverse('mytrack:is_come')
        return redirect(link)

        # return JsonResponse({
        #     'status': 200,
        #     'type': 'success',
        #     'message': "La charge virale a été ajoutée", 
        #     'redirectLink': {
        #         'link': link,
        #     }, 
        # })

    motif = ['ARV', 'CV', 'ETP',]

    motif.sort()
    context = {'motif':motif}

    return render(request, 'mytrack/respect_temps/venue.html', context)

def edit_respect(request, code_respect):
    respect_json = Respect.objects.filter(account=request.user).first()
    respect_list = json.loads(respect_json.info_respect_rdv)
    rest_respect = None
    if request.method=="POST":
        data = request.POST
        print(data)
        code_respect=data["code_respect"]
        for respect in respect_list:
            if code_respect==respect["code_respect"]:
                respect['date']=data['relance_date']
                respect['code_patient']=data['patient_code']
                respect['reason']=', '.join(data.getlist('motif'))
                respect['comment']=data['respect_comment']
        respect_json.info_respect_rdv=json.dumps(respect_list)
        respect_json.save()

        link = reverse('mytrack:is_come')
        return redirect(link)
    for respect in respect_list:
        if code_respect==respect["code_respect"]:
            rest_respect = respect
        
    motif = ['ARV', 'CV', 'ETP',]
    motif.sort()

    context = {'motif':motif, 'respect':rest_respect}

    return render(request, 'mytrack/respect_temps/edit_respect.html', context)




def show_forms(request):
    return render(request, 'mytrack/index.html')


#VUES INDEX
def add_index(request):
    if request.method == "POST":
        form_data = request.POST
        type_contact = form_data['type_contact']
        if type_contact == 'other':
            type_contact = form_data['type_contact_other']
        infos_index ={
        'code_index' : secrets.token_hex(8),
        'patient_code' : form_data['patient_code'],
        'contact_code' : f"{form_data['patient_code']}-{secrets.token_hex(2).upper()}",
        'type_contact' : type_contact,
        'sexe_contact' : form_data['sexe_contact'],
        'date_naissance' : form_data['date_naissance'],
        'statut_identification' : form_data['statut_identification'],
        'is_archive': False,
        }
        

        account_index = FicheIndex.objects.filter(account=request.user).first()
        account_index_infos_index = []

        if account_index:
            account_index_infos_index = json.loads(account_index.info_index, encoding="utf-8")
            account_index_infos_index.append(infos_index)
            account_index.info_index = json.dumps(account_index_infos_index)
            account_index.save()
        else:
            account_index_infos_index.append(infos_index)
            FicheIndex.objects.create(account=request.user, info_index=json.dumps(account_index_infos_index))


        link = reverse('mytrack:list_index')
        return redirect(link)

        # return JsonResponse({
        #     'status': 200,
        #     'type': 'success',
        #     'message': "L'index a été ajoutée", 
        #     # 'redirectLink': {
        #     #     'link': link,
        #     # }, 
        # })


    sexe_contact = ['Masculin', 'Feminin', 'Transgenre',]
    statut_identification = ['VIH +', 'VIH -', 'Inconnu']
    type_contact = ['Conjoint', 'Autre partenaire sexuel', 'Enfant biologique < 15 ans', 'Frères /Sœurs   < 15 ans (de index < 15 ans)', "Père/Mère(de l'index < 15 ans)",]

    sexe_contact.sort()
    type_contact.sort()
    statut_identification.sort()

    context = {'sexe_contact': sexe_contact, 'type_contact': type_contact, 'statut_identification': statut_identification}
    return render(request, "mytrack/index_temps/add_index.html", context)


def edit_index(request, code_index):
    index = FicheIndex.objects.filter(account=request.user).first()
    persons_index = load_info(index.info_index)
    emp_index = None
    if request.method == "POST":
        data = request.POST
        print(data)
        code_index = data["code_index"]
        type_contact = data['type_contact']
        if type_contact == 'other':
            type_contact = data['type_contact_other']
        for i in persons_index:
            if i["code_index"]==code_index:
                if i['patient_code']!=data["patient_code"]:
                    i["contact_code"]=f"{data['patient_code']}-{secrets.token_hex(2).upper()}"
                i["patient_code"]=data["patient_code"]
                i["type_contact"]=type_contact
                i["sexe_contact"]=data["sexe_contact"]
                i["date_naissance"]=data["date_naissance"]
                i["statut_identification"]=data["statut_identification"]
        index.info_index = json.dumps(persons_index)
        index.save()
        link = reverse('mytrack:list_index')
        return redirect(link)

        # return JsonResponse({
        #     'status': 200,
        #     'type' : 'success',
        #     'message' : 'Les informations de l'index ont été modifiée',
        #     'redirectLink' : {
        #         'link':link,
        #     },
        # })
    for ind in persons_index:
        if ind["code_index"] == code_index:
            emp_index = ind
            break
    
    sexe_contact = ['Masculin', 'Feminin', 'Transgenre',]
    statut_identification = ['VIH +', 'VIH -', 'Inconnu']
    type_contact = ['Conjoint', 'Autre partenaire sexuel', 'Enfant biologique < 15 ans', 'Frères /Sœurs   < 15 ans (de index < 15 ans)', "Père/Mère(de l'index < 15 ans)",]

    sexe_contact.sort()
    type_contact.sort()
    statut_identification.sort()
    
    context = {'per_index':emp_index,'sexe_contact': sexe_contact, 'type_contact': type_contact, 'statut_identification': statut_identification }
    return render(request, 'mytrack/index_temps/edit_index.html', context)

    # LIST DES CONTACTS


def list_index(request):
    fiche_index = FicheIndex.objects.filter(account=request.user).first()
    index = []

    if fiche_index:
        index = json.loads(fiche_index.info_index)
        
    
    context = {'index': index}
    return render(request, 'mytrack/index_temps/list_contact_index.html', context)
    
    


#VUES RENDEZ-VOUS

def add_rdv(request):
    if request.method == "POST":
        form_data = request.POST
        
        infos_rdv ={
        'code_rdv':secrets.token_hex(8),
        'patient_code' : form_data['patient_code'],
        'motif' :', '.join(form_data.getlist('motif')) ,
        'date_rdv' : form_data['date_rdv'],
        'is_archive': False,
        }
        account_rdv = FicheRdv.objects.filter(account=request.user).first()
        account_rdv_infos_rdv = []

        if account_rdv:
            account_rdv_infos_rdv = json.loads(account_rdv.info_rdv, encoding="utf-8")
            account_rdv_infos_rdv.append(infos_rdv)
            account_rdv.info_rdv = json.dumps(account_rdv_infos_rdv)
            account_rdv.save()
        else:
            account_rdv_infos_rdv.append(infos_rdv)
            FicheRdv.objects.create(account=request.user, info_rdv=json.dumps(account_rdv_infos_rdv))


        link = reverse('mytrack:list_rdv')
        # return redirect(link)

        return JsonResponse({
            'status': 200,
            'type': 'success',
            'message': "L'index a été ajoutée", 
            'redirectLink': {
                'link': link,
            }, 
        })


    motif = ['ARV', 'CV', 'ETP',]

    motif.sort()

    context = {'motif': motif}
    return render(request, "mytrack/rdv_temps/add_rdv.html", context)



def edit_rdv(request, code_rdv):
    all_rdv=FicheRdv.objects.filter(account=request.user).first()
    list_rdv=json.loads(all_rdv.info_rdv)
    cur_rdv = None
    if request.method=="POST":
        data = request.POST
        code_rdv=data['code_rdv']
        for i in list_rdv:
            if i["code_rdv"]==code_rdv:
                i["patient_code"]=data["patient_code"]
                i["motif"]=', '.join(data.getlist('motif'))
                i["date_rdv"]=data["date_rdv"]
        all_rdv.info_rdv = json.dumps(list_rdv)
        all_rdv.save()

        link = reverse('mytrack:list_rdv') 

        return JsonResponse({
            'status': 200,
            'type': 'success',
            'message': "L'index a été ajoutée", 
            'redirectLink': {
                'link': link,
            }, 
        })
    for rdv in list_rdv:
        if rdv['code_rdv'] == code_rdv:
            cur_rdv = rdv
            break

    motif = ['ARV', 'CV', 'ETP',]
    motif.sort()
    context = {'rdvm':cur_rdv,'motif': motif}

    return render(request, "mytrack/rdv_temps/edit_rdv.html", context)





#LIST DES RENDEZ-VOUS FIXES


def list_rdv(request):
    fiche_rdv = FicheRdv.objects.filter(account=request.user).first()
    rdv = []

    if fiche_rdv:
        rdv = json.loads(fiche_rdv.info_rdv)
        
    
    context = {'rdv': rdv}
    return render(request, 'mytrack/rdv_temps/list_rendez_vous.html', context)

# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]

#     for row in cursor.fetchall():
#         yield dict(zip(columns, row))



# def form(request):
#     return render(request, "mytrack/test.html")

# def rupture(request):
#     if request.method == "POST":
#         cp = request.POST['patient_code']
#         print(cp)
#         with connections['sigdep'].cursor() as cursor:
#             query = '''
#             SELECT pi.identifier as patient_code, pn.family_name as first_name
#             FROM patient_identifier as pi,person_name as pn
#             WHERE pi.person_id = %s
#             '''
#             cursor.execute(query,cp)
#             row = list(dictfetchall(cursor))
#         var = row[0]
#         print(var)
#     link = reverse('mytrack:list_rdv')
#     return redirect(link)