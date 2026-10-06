from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.

class Expedition(models.Model):
    reference = models.CharField(max_length=20 , unique= True , editable= False )
    poids_kg= models.DecimalField(max_digits=6,decimal_places=2)
    status= models.CharField(max_length=100, choices= [
        {'publiee','Publiee'},
        {'attribuee','Attrinuee'},
        {'en_cours','En_cours'},
        {'livree','Livree'},
        {'annulee','Annulee'},
    ],default='publiee')
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    date_souhaitee=models.DateField()
    description = models.TextField()
    entreprise= models.ForeignKey(Entreprise,on_delete=models.CASCADE , related_name='expeditions' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise == 'chargeur':
            raise ValidationError({'entreprise':'une expedition ne peut etre que par une entreprise de type chargeur'})


    


    @classmethod
    def _generte_reff(cls):
        annee = timezone.now().strftime("%y")
        last = cls.objects.filter(reference__startswith=f'EXP_{annee}_').order_by('-reference').first()
        compteur = int(last.reference[-5:])+1 if last else 1
        if compteur >99999:
            raise ValidationError("Limite exceded")
        return f"EXP_{annee}_{compteur:05d}"

    def save(self , *args , **kwargs):
        if not self.reference:
            self.reference = self._generte_reff
        self.full_clean()
        super().save(*args,**kwargs)