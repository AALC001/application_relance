from django.urls import path
from . import views

#ecriture des urls
app_name = 'authentication'
urlpatterns = [
    path('', views.index, name ='index'),
    path('create/', views.create, name = 'create'),
    path('set_user_inactive/', views.set_user_inactive, name='set_user_inactive'),
    path('set_user_active/', views.set_user_active, name='set_user_active'),
    path('delete/', views.delete, name = 'delete'),
    path("show/<int:pk>", views.show_user, name="show"),
]