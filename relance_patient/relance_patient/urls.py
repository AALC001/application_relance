"""relance_patient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import login_view, logout_view, profile, profile_set_password, profile_set_info
from dashboard.views import handle_404, handle_500, handle_403

urlpatterns = [
    path('', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('mytrack/', include('mytrack.urls')),
    path('users/', include('authentication.urls')),
    path('accounts/login/',login_view, name = 'authentication_login'),
    path('accounts/logout/',logout_view, name = 'authentication_logout'),
    path('profile/', profile, name="authentication_profile"),
    path('profile/set_password', profile_set_password, name="authentication_profile_set_password"),
    path('profile/set_info', profile_set_info, name="authentication_profile_set_info"),
    path('patient-listing/', include('patientlisting.urls')),
    path('relance/', include('activite_relance.urls')),
    path('not-found/', handle_404),
    path('not-allow/', handle_403),
    path('error-server/', handle_500),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
