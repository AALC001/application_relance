import secrets
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Account
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from global_login_required import login_not_required
from django.views.decorators.csrf import csrf_protect
from dashboard.models import SiteInfo

# Show all users
def index(request):
    accounts = []
    sites = SiteInfo.objects.all()
    if request.user.is_super:
        accounts = Account.objects.filter(is_admin=True, is_super=False)
    else:
        accounts = User.objects.filter(site_code=request.user.user.site_code).exclude(pk=request.user.pk)

    count = accounts.count()
    context = {
        'accounts': accounts,
        'date': timezone.localdate().year,
        'request': request.resolver_match,
        'sites': sites,
        'count': count
    }
    return render(request, 'authentication/index.html', context)


# Create user
def create(request):
    if request.method == 'POST':
        form_data = request.POST
        email = form_data['email']
        # password = form_data['password1']
        first_name = form_data['first_name']
        last_name = form_data['last_name']
        site_code = ""
        contact = form_data['contact']
        user_code = 'USER' + secrets.token_hex(6).upper()
        is_admin = False
        default_password = "as@2020!"

        if form_data['role_admin'] == "true":
            is_admin = True

        if request.user.is_super:
            site_code = form_data['site_code']
        else:
            site_code = request.user.user.site_code

        if(Account.objects.filter(email=email).exists()):
            return JsonResponse({
                'status': 404,
                'type': 'error',
                'error': {
                    'label': 'email',
                    'title': "Erreur email",
                    'message': "L'email est déjà utilisé",
                }
            })

        account = Account.objects.create_user(email=email)
        account.is_admin = is_admin
        account.set_password(default_password)
        account.save()

        user = User(account=account, user_code=user_code, first_name=first_name, last_name=last_name, contact=contact, site_code=site_code)
        user.save()

        link = reverse('authentication:index')
        # users = User.objects.all()

        return JsonResponse({
            'status': 200,
            'type': 'success',
            'message': "Le compte de l'utilisateur a été créé",
            'redirectLink': {
                'link': link,
                # 'params': users
            },
        })

    sites = []

    for site in SiteInfo.objects.all():
        if site.site_admin is None:
            sites.append(site)

    return render(request, 'authentication/create.html', {'sites':sites})


# Delete user
def delete(request):
    data = request.POST
    Account.objects.filter(pk=int(data["user_id"])).delete()
    return JsonResponse({
        'type': 'success',
        'message': "L'utlisateur a été supprimé"
    })


# Deactivate user
def set_user_inactive(request):
    data = request.POST
    print(data)
    account = Account.objects.filter(pk=int(data["user_id"])).first()
    account.is_active = False
    account.save()
    return JsonResponse({'type':'success', 'message': "Le compte de l'utilisateur a été désactivé"})


# Acrivate user
def set_user_active(request):
    data = request.POST
    account = Account.objects.filter(pk=int(data["user_id"])).first()
    account.is_active = True
    account.save()
    return JsonResponse({'type':'success', 'message': "Le compte de l'utilisateur a été activé"})


# Show user
def show_user(request, pk):
    user = User.objects.filter(pk = pk).first()
    if user:
        content = {
            'firstName': user.first_name,
            'lastName': user.last_name,
            'contact': user.contact,
            'email': user.account.email,
        }

        return JsonResponse({
            "type": "success",
            "content": content
        })
    return JsonResponse({'type': 'error', 'message': 'Une erreur est souvenue, veuillez réessayer'})


# User Profile
def profile(request):
    account = request.user
    context = {'account': account}
    return render(request, 'authentication/profile.html', context=context)

# Update user profile password
def profile_set_password(request):
    account = request.user
    account.set_password(request.POST['password1'])
    account.first_connection = False
    account.save()
    messages.add_message(request,messages.INFO, 'Mot de passe modifié, veuillez vous reconnecté')
    return JsonResponse({'type': 'success', 'message': 'Modification du mot de passe réussie'})


# update user profile general infos
def profile_set_info(request):
    form_data = request.POST
    email = form_data['email']
    first_name = form_data['first_name']
    last_name = form_data['last_name']
    contact = form_data['contact']

    if Account.objects.exclude(pk=request.user.pk).filter(email=email):
        return JsonResponse({
            'status': 404,
            'type': 'error',
            'error': {
                'label': 'email',
                'title': "Erreur email",
                'message': "L'email est déjà utilisé",
            }
        })
    else:
        account = Account.objects.get(pk=request.user.pk)
        account.email = email
        account.save()

        user = User.objects.filter(account=account).first()
        if user == None:
            user_code = 'USER' + secrets.token_hex(6).upper()
            user = User(account = account, user_code = user_code, last_name = last_name, first_name=first_name, contact = contact)
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.contact = contact
        user.save()

    return JsonResponse({
        'status': 200,
        'type': 'success',
        'message': "Modification du profile réussie",
        'redirectLink': {
            'link': 'profile'
        },
    })

# User login
def login_view(request):
    if request.method == 'POST':
        form_data = request.POST
        email = form_data['auth-email']
        password = form_data['auth-password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'type': 'success',
                'redirectLink': reverse('dashboard:home')
            })
        else:
            return JsonResponse({
                'type': 'error',
                'message': 'Email ou mot de passe incorrecte'
            })
    return render(request,'authentication/login.html')


# User logout
def logout_view(request):
    logout(request)
    return redirect(reverse('authentication_login'))
