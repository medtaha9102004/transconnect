from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.validators import MinValueValidator
# Create your models here.

class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=100, unique=True)
    capacite_kg= models.PositiveIntegerField(validators=[MinValueValidator(1,"le capacite doit etre > 0 kg")])
    type_v = models.CharField(max_length=100, choices= [
        {'camionnette','Camionnette'},
        {'fourgon','Fourgon'},
        {'camion porteur','Camion Porteur'},
        {'semi-remorque','Semi-Remorque'},
    ])
    disponible = models.BooleanField()
    entreprise = models.ForeignKey(Entreprise , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
