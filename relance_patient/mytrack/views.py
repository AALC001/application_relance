import json
import secrets
import datetime as dt
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from .models import Respect, FicheIndex, FicheRdv
# Create your views here. 

def load_info(info:str) -> list:
    return json.loads(info)

def get_not_archive_info(info:str) -> list:
    return [data for data in info if not data['is_archive']]

def get_archive_info(info) -> list:
    return [data for data in info if data['is_archive']]

# def list_charge_virale(request):
#     cv = ChargeVirale.objects.filter(account=request.user).first()
#     charge_virale = []
#     if cv:
#         charge_virale = json.loads(cv.info_charge_virale)
        
#     context = {'charge_virale': charge_virale}
#     return render(request, 'mytrack/show_list_cv.html', context)

def list_is_come(request):
    venue = Respect.objects.filter(account=request.user).first()
    come = []
    if venue:
        come = get_not_archive_info(json.loads(venue.info_respect_rdv))
        
    context = {'come': come}
    return render(request, 'mytrack/respect_temps/list_venue.html', context)


# def add_charge_virale(request):
#     if request.method=="POST":
#         form_data = request.POST
#         info_charge_virale = {
#             'cv_code': secrets.token_hex(8),
#             'cv_date': form_data['relance_date'],
#             'code_patient':form_data['patient_code'],
#             'result_charge':int(form_data['charge_virale']),
#             'comment':form_data['charge_comment'],
#             'is_archive': False,
#         }
        
#         charge_virale = ChargeVirale.objects.filter(account=request.user).first()
#         info_charge = []
#         if charge_virale:
#             info_charge = json.loads(charge_virale.info_charge_virale, encoding="utf-8")
#             info_charge.append(info_charge_virale)
#             charge_virale.info_charge_virale = json.dumps(info_charge)
#             charge_virale.save()
#         else:
#             info_charge.append(info_charge_virale)
#             ChargeVirale.objects.create(account=request.user, info_charge_virale=json.dumps(info_charge))

#         link = reverse('mytrack:listing_charge_virale')
#         return JsonResponse({
#             'status': 200,
#             'type': 'success',
#             'message': "La relance a été modifiée", 
#             'redirectLink': {
#                 'link': link,
#             }, 
#         })
#         # return redirect(link)
        
#     return render(request, 'mytrack/add_charge_virale.html')

def respect_rdv(request):
    if request.method=='POST':
        form_data = request.POST
        info_respect = {
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
    print(list_rdv)
    if request.method=="POST":
        data = request.POST
        code_rdv=data['code_rdv']
        for i in list_rdv:
            if i["code_rdv"]==code_rdv:
                i["patient_code"]=data["patient_code"]
                i["motif"]=', '.join(data.getlist('motif'))
                i["date_rdv"]=data["date_rdv"]
        all_rdv.info_rdv = json.loads(list_rdv)
        all_rdv.save()

        link = reverse('mytrack:list_rdv')
        return redirect(link) 

        # return JsonResponse({
        #     'status': 200,
        #     'type': 'success',
        #     'message': "L'index a été ajoutée", 
        #     'redirectLink': {
        #         'link': link,
        #     }, 
        # })
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

# def edit_charge_virale(request, cv_code):
#     cv = ChargeVirale.objects.filter(account=request.user).first()
#     charge_virale = load_info(cv.info_charge_virale)
#     cur_cv = None

#     if request.method == "POST":
#         data = request.POST
#         cv_code=data["cv_code"]

#         for cv in charge_virale:
#             if cv['cv_code'] == cv_code:
#                 cv['cv_date'] == data['relance_date']
#                 cv['code_patient'] == data['patient_code']
#                 cv['result_charge'] == data['charge_virale']
#                 cv['comment'] == data['charge_comment']
#         cv.info_charge_virale = json.dumps(charge_virale)
#         cv.save()
#         link = reverse('mytrack:listing_charge_virale')
#         return JsonResponse({
#             'status': 200,
#             'type' : 'success',
#             'message' : 'Les informations de charge virale ont été modifiée',
#             'redirectLink' : {
#                 'link':link,
#             },
#         })
#     for cv in charge_virale:
#         if cv['cv_code'] == cv_code:
#             cur_cv = cv
#             break

#     context = {'charge_virale':cur_cv}
#     return render(request, 'mytrack/edit_cv.html/', context)