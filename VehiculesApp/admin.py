from django.contrib import admin
from .models import Vehicule


class VehiculeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'immatriculation',
        'type_v',
        'capacite_kg',
        'disponible',
        'entreprise',
        'created_at',
    )

    list_filter = ("type_v", "disponible")

    search_fields = (
        "immatriculation",
        "entreprise__raison_sociale",
    )

    list_select_related = ("entreprise",)

    readonly_fields = (
        'id',
        'created_at',
    )

    fieldsets = (
        ("Informations du véhicule", {
            "fields": (
                "id",
                "immatriculation",
                "type_v",
                "capacite_kg",
            ),
        }),
        ("Disponibilité et entreprise", {
            "fields": (
                "disponible",
                "entreprise",
            ),
        }),
        ("Horodatage", {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )


admin.site.register(Vehicule, VehiculeAdmin)
