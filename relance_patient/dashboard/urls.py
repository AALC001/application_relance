from django.urls import path
from . import views

app_name='dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('site-list/', views.site_list, name='site_list'),
    path('site-list/create/', views.site_create, name='site_create'),
    path('site-list/delete/', views.site_delete, name='site_delete'),
    path('site-list/edit/<int:pk>', views.site_edit, name='site_edit'),
    path('site-list/attribute', views.site_edit, name='site_attribute'),
    path('api/relances/', views.ListRelances.as_view()),
]
