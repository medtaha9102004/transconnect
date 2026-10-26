from django.urls import path
from .views import *
app_name = 'ExpeditionsApp'
urlpatterns = [
     path('home/',home, name='home'),
     path('afficher/<str:name>/', afficher, name='afficher'),
     path('list/', listExpeditions, name='listExpeditions'),
     path('detail/<int:pk>/', detailExpedition, name='detailExpedition'),
]