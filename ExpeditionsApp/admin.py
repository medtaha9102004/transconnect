from datetime import timedelta

from django.contrib import admin, messages
from django.db.models import Count, Q
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone

from .models import Expedition
from OffresApp.models import Offre
from EntreprisesApp.models import Entreprise
from VehiculesApp.models import Vehicule


# Filtre pour afficher uniquement les expéditions en retard
class EnRetardFilter(admin.SimpleListFilter):
    title = "En retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return (
            ("oui", "Oui"),
            ("non", "Non"),
        )

    def queryset(self, request, queryset):
        aujourd_hui = timezone.localdate()

        if self.value() == "oui":
            return queryset.filter(
                status="publiee",
                date_souhaitee__lt=aujourd_hui
            )

        if self.value() == "non":
            return queryset.exclude(
                status="publiee",
                date_souhaitee__lt=aujourd_hui
            )

        return queryset


# Affichage des offres dans la page d'une expédition
class OffreInline(admin.TabularInline):
    model = Offre
    extra = 0
    fields = (
        "transporteur",
        "vehicule",
        "prix",
        "delai_jour",
        "status",
        "date_proposition",
    )
    readonly_fields = ("date_proposition",)


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "ville_depart",
        "ville_arrivee",
        "poids_kg",
        "date_souhaitee",
        "statut_colore",
        "entreprise",
        "created_at",
    )

    list_filter = (
        "status",
        "date_souhaitee",
        EnRetardFilter,
    )

    search_fields = (
        "reference",
        "ville_depart",
        "ville_arrivee",
        "entreprise__raison_sociale",
    )

    readonly_fields = (
        "reference",
        "created_at",
        "updated_at",
    )

    list_select_related = ("entreprise",)

    inlines = [OffreInline]

    actions = ["cloturer_expeditions"]

    @admin.display(description="Statut")
    def statut_colore(self, obj):
        couleurs = {
            "publiee": "#F0AD4E",
            "attribuee": "#337AB7",
            "en_cours": "#5BC0DE",
            "livree": "#5CB85C",
            "annulee": "#D9534F",
        }

        couleur = couleurs.get(obj.statut, "#777777")

        from django.utils.html import format_html

        return format_html(
            '<span style="background-color:{}; color:white; '
            'padding:3px 8px; border-radius:4px;">{}</span>',
            couleur,
            obj.get_statut_display(),
        )

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        nombre = queryset.filter(status="en_cours").update(
            status="livree"
        )

        self.message_user(
            request,
            f"{nombre} expédition(s) passée(s) au statut Livrée.",
            level=messages.SUCCESS,
        )

    # Ajouter une URL personnalisée à l'administration des expéditions
    def get_urls(self):
        urls = super().get_urls()

        urls_personnalisees = [
            path(
                "health-check/",
                self.admin_site.admin_view(self.health_check_view),
                name="expedition-health-check",
            ),
        ]

        return urls_personnalisees + urls

    # Vue du tableau de bord de contrôle d'intégrité
    def health_check_view(self, request):
        limite = timezone.now() - timedelta(days=7)

        # 1. Une offre proposée doit être liée à une expédition publiée.
        # Une offre acceptée doit être liée à une expédition attribuée.
        offres_incoherentes = (
            Offre.objects
            .filter(
                Q(status="proposee")
                & ~Q(expedition__status="publiee")
                |
                Q(status="acceptee")
                & ~Q(expedition__status="attribuee")
            )
            .select_related("expedition", "transporteur")
        )

        # 2. Expéditions publiées depuis plus de sept jours
        expeditions_anciennes = Expedition.objects.filter(
            status="publiee",
            created_at__lt=limite,
        )

        # 3. Entreprises de transport sans véhicule
        transporteurs_sans_vehicule = (
            Entreprise.objects
            .filter(type_entreprise="transporteur")
            .annotate(nb_vehicules=Count("vehicules"))
            .filter(nb_vehicules=0)
        )

        # 4. Véhicules disponibles associés à une offre acceptée
        vehicules_incoherents = (
            Vehicule.objects
            .filter(
                disponibilite=True,
                offres__statut="acceptee",
            )
            .distinct()
        )

        # 5. Plusieurs offres proposées par le même transporteur
        # pour la même expédition
        propositions_doubles = (
            Offre.objects
            .filter(status="proposee")
            .values(
                "expedition__reference",
                "transporteur__raison_sociale",
            )
            .annotate(nb_offres=Count("id"))
            .filter(nb_offres__gt=1)
        )

        context = {
            **self.admin_site.each_context(request),
            "title": "Tableau de bord de contrôle d'intégrité",
            "offres_incoherentes": offres_incoherentes,
            "expeditions_anciennes": expeditions_anciennes,
            "transporteurs_sans_vehicule": transporteurs_sans_vehicule,
            "vehicules_incoherents": vehicules_incoherents,
            "propositions_doubles": propositions_doubles,
        }

        return TemplateResponse(
            request,
            "admin/health_check.html",
            context,
        )