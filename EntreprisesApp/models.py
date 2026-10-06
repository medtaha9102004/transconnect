from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator 

# Create your models here.
def Email_validator(value):
    if not value:
        raise ValidationError("l'address email est obligatoire")
    if not value.endswith("@gmail.com"):
        raise ValidationError("domaine invalid")
class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, editable=False , primary_key=True)
    email = models.EmailField(unique=True,validators=[Email_validator])
    telephone = models.CharField(max_length=15 , null=True , blank=True)
    role = models.CharField(max_length=20 , choices=[
        {'chargeur','Chargeur'},
        {'trasporteur','Transporteur'},
         {'administrateur','Administrateur'},
    ],default='chargeur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
matrucile_fiscal_validator = RegexValidator(regex=r'\d[17][/ -]?[a-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
                                                message="fromat non confirmee")

class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, null=False , blank=False)
    mat_fisc = models.CharField(max_length=17 , null= False , blank = False , unique= True , validators=[matrucile_fiscal_validator])
    adresse = models.TextField(validators=[MinLengthValidator(20 ,"address length must be greater than 20 car")])
    type_entreprise = models.CharField(max_length=100, choices=[
        {'chargeur','Chargeur'},
        {'trasporteur','Transporteur'}
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gerant = models.OneToOneField(Utilisateur , on_delete= models.CASCADE,related_name='entreprise')
