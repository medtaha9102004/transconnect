
from django.contrib import admin
from django.utils.html import format_html
from .models import Offre
import csv
from django.http import HttpResponse


@admin.action(description="Exporter la sélection en CSV")
def exporter_offres_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="offres.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "reference_expedition",
        "transporteur",
        "prix",
        "status",
    ])

    for offre in queryset.select_related("expedition", "transporteur"):
        writer.writerow([
            offre.expedition.reference,
            str(offre.transporteur),
            offre.prix,
            offre.status,
        ])

    return response


class PrixOffreFilter(admin.SimpleListFilter):
    title = 'Prix de l’offre'
    parameter_name = 'prix_offre'

    def lookups(self, request, model_admin):
        return [
            ('economique', 'Prix inférieur à 500'),
            ('moyen', 'Prix entre 500 et 1000'),
            ('eleve', 'Prix supérieur à 1000'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'economique':
            return queryset.filter(prix__lt=500)

        if self.value() == 'moyen':
            return queryset.filter(prix__gte=500, prix__lte=1000)

        if self.value() == 'eleve':
            return queryset.filter(prix__gt=1000)

        return queryset


class OffreAdmin(admin.ModelAdmin):
    actions = [exporter_offres_csv]

    list_display = (
        'id',
        'expedition',
        'transporteur',
        'vehicule',
        'prix',
        'delai_jour',
        'status',
        'date_proposition',
        'created_at',
        'status_colore',
    )

    list_filter = (
        'status',
        'date_proposition',
        PrixOffreFilter,
    )

    search_fields = (
        'expedition__reference',
        'transporteur__username',
        'vehicule__immatriculation',
    )

    readonly_fields = (
        'id',
        'date_proposition',
        'created_at',
        'updated_at',
    )

    list_select_related = (
        'expedition',
        'transporteur',
        'vehicule',
    )

    fieldsets = (
        ('Informations générales', {
            'fields': (
                'id',
                'expedition',
                'transporteur',
            ),
        }),
        ("Véhicule et conditions de l'offre", {
            'fields': (
                'vehicule',
                'prix',
                'delai_jour',
            ),
        }),
        ('status et horodatage', {
            'fields': (
                'status',
                'date_proposition',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    autocomplete_fields = (
    "expedition",
    "transporteur",
    "vehicule",
)

    @admin.display(description="status")
    def status_colore(self, obj):
        couleurs = {
            "proposee": "#F0AD4E",
            "acceptee": "#5CB85C",
            "refusee": "#D9534F",
            "retiree": "#777777",
        }

        couleur = couleurs.get(obj.status, "#999999")

        return format_html(
            '<span style="background-color:{}; color:white; '
            'padding:3px 8px; border-radius:4px;">{}</span>',
            couleur,
            obj.get_status_display()
        )

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)

        if obj and obj.status == 'acceptee':
            return base + ['prix', 'delai_jour']

        return base


admin.site.register(Offre, OffreAdmin)
