from django.db import models
from django.core.exceptions import ValidationError
from EntreprisesApp.models import Entreprise
from VehiculesApp.models import Vehicule
from ExpeditionsApp.models import Expedition
from django.core.validators import MinValueValidator
from django.db import models,transaction
# Create your models here.

class Offre(models.Model):
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

    def clean(self):
        super().clean()

        # Le transporteur doit être une entreprise de type transporteur
        if (
            self.transporteur_id
            and self.transporteur.type_entreprise != 'transporteur'
        ):
            raise ValidationError({
                'transporteur': (
                    "L'entreprise doit être de type transporteur."
                )
            })

        # Le véhicule doit appartenir au transporteur de l'offre
        if (
            self.vehicule_id
            and self.transporteur_id
            and self.vehicule.entreprise_id != self.transporteur_id
        ):
            raise ValidationError({
                'vehicule': (
                    "Le véhicule doit appartenir au transporteur de l'offre."
                )
            })

        # Une nouvelle offre nécessite une expédition publiée
        if (
            self._state.adding
            and self.expedition_id
            and self.expedition.statut != 'publiee'
        ):
            raise ValidationError({
                'expedition': (
                    "Une offre ne peut être créée que pour "
                    "une expédition publiée."
                )
            })

        # Une entreprise ne peut pas avoir deux offres proposées
        # simultanément sur la même expédition
        if (
            self.statut == 'proposee'
            and self.expedition_id
            and self.transporteur_id
        ):
            offres_existantes = Offre.objects.filter(
                expedition_id=self.expedition_id,
                transporteur_id=self.transporteur_id,
                statut='proposee'
            )

            if self.pk:
                offres_existantes = offres_existantes.exclude(pk=self.pk)

            if offres_existantes.exists():
                raise ValidationError({
                    'transporteur': (
                        "Ce transporteur possède déjà une offre proposée "
                        "pour cette expédition."
                    )
                })

        # Un véhicule indisponible ne peut pas être proposé
        # dans une nouvelle offre
        if (
            self._state.adding
            and self.statut == 'proposee'
            and self.vehicule_id
            and not self.vehicule.disponibilite
        ):
            raise ValidationError({
                'vehicule': "Ce véhicule n'est pas disponible."
            })

        # Vérification du poids selon le type du véhicule
        if self.expedition_id and self.vehicule_id:
            poids = self.expedition.poids_kg
            capacite = self.vehicule.capacite_kg
            type_vehicule = self.vehicule.type_vehicule

            if poids > capacite:
                raise ValidationError({
                    'vehicule': (
                        "La capacité du véhicule est insuffisante "
                        "pour cette expédition."
                    )
                })

            limites = {
                'camionnette': (0, 1500),
                'camion_porteur': (3500, 19000),
                'semi_remorque': (19000, 26000),
                'fourgon': (0, 3500),
            }

            if type_vehicule in limites:
                minimum, maximum = limites[type_vehicule]

                if poids < minimum or poids > maximum:
                    raise ValidationError({
                        'vehicule': (
                            "Le type de véhicule n'est pas compatible "
                            "avec le poids de cette expédition."
                        )
                    })
    def save(self, *args, **kwargs):
        with transaction.atomic():
            anicent_statut=None
            if self.pk :
                ancienne_offre=Offer.objects.get(pk=self.pk)
                anicent_statut=ancienne_offre.statut
                self.expedition.statut='attribuee'
                self.expedition.save()
                Offer.objects.filter(expedition_id=self.expedition_id,statut='proposee').exclude(pk=self.pk).update(statut='refusee')
        self.full_clean()
        super().save(*args, **kwargs)
        def __str__(self):
            return f"Offre - {self.expedition.reference} - {self.transporteur.raison_sociale}"            