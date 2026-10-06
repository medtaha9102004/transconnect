from django.db import models
from EntreprisesApp.models import Entreprise
from VehiculesApp.models import Vehicule
from ExpeditionsApp.models import Expedition
# Create your models here.

class Offer(models.Model):
    prix = models.DecimalField(max_digits=6 , decimal_places=2)
    delai_jour = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[
        {'proposee','Proposee'},
        {'acceptee','Acceptee'},
        {'refusee','Refusee'},
        {'retiree','Retiree'},
    ],default='proposee')
    date_proposition = models.DateField(auto_now_add=True)
    expedition = models.ForeignKey(Expedition , on_delete=models.CASCADE)
    transporteur = models.ForeignKey(Entreprise , on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)