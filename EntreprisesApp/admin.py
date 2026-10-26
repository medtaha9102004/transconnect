from django.contrib import admin
from django.contrib.admin import site

from VehiculesApp.models import Vehicule
from .models import Utilisateur,Entreprise
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class VehiculeInline(admin.TabularInline):
    model = Vehicule
    extra = 0
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username',
'email', 'telephone', 'role', 'telephone','is_active', 'created_at')
    list_filter = ('role', 'is_active')
    readonly_fields = ('user_id', 'date_joined', 'last_login', 'created_at','updated_at')
class EntrepriseAdmin (admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display = ('raison_sociale', 'mat_fisc', 'adresse', 'type_entreprise', 'gerant', 'created_at')
    list_filter = ("type_entreprise",)

    search_fields = (
        "raison_sociale",
        'mat_fisc',
        'type_entreprise',
        'gerant',
        'created_at',
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "raison_sociale",
                "mat_fisc",
                "type_entreprise",
            ),
        }),
        ("Gestion de l'entreprise", {
            "fields": (
                "gerant",
                "adresse",
            ),
        }),
        ("Horodatage", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)    
admin.site.register(Entreprise, EntrepriseAdmin)
