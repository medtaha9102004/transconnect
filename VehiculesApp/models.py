from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
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
    disponible = models.BooleanField(default=True)
    entreprise = models.ForeignKey(Entreprise , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()
        if(self.entreprise_id and self.entreprise.type_entreprise !='transporteur'):
            raise ValidationError('l  entreprise doit etre de type transporteur')

    def save(self ,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)
        def __str__(self):
            return f"{self.immatriculation} - {self.get_type_vehicule_display()}"    