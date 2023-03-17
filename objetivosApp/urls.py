from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('actividad/', views.actividad, name='actividad'),
    path('objetivos/', views.objetivos, name='objetivos'),
    path('cumplir/<int:id>/', views.cumplir, name='cumplir'),
    path('reporte' , views.reporte, name='reporte'),
    path('integrantes/', views.integrantes, name='integrantes'),
    path('accounts/logout/', views.logout, name='logout'),
    path('registrar/', views.registrar, name='registrar'),
    path('registro/', views.registro, name='registro'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar')
]