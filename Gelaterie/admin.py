from django.contrib import admin
from .models import (
    Adresa, Alergeni, Bauturi, Inghetata, Biscuite, Prajituri, 
    Torturi_Inghetata, Meniu, Comanda, Informatii, Sponsor, Magazine
)

# Personalizare pagina de administrare
admin.site.site_header = "Gelaterie Admin"
admin.site.site_title = "Gelaterie Admin Portal"
admin.site.index_title = "Administrare Gelaterie"

# Filtru lateral pentru Prajituri
class PrajituriAdmin(admin.ModelAdmin):
    search_fields = ['nume_prajitura']
    list_filter = ['nume_prajitura']  # Adaugati filtre laterale pentru minim un model

# Impărtirea câmpurilor în secțiuni pentru Comanda
class ComandaAdmin(admin.ModelAdmin):
    search_fields = ['data_achizitie']
    fieldsets = (
        ("Informații Generale", {
            'fields': ('data_achizitie', 'livrare_curier')
        }),
        ("Detalii Produs", {
            'fields': ('informatii',)
        }),
    )

class AdresaAdmin(admin.ModelAdmin):
    search_fields = ['tara', 'oras']

class AlergeniAdmin(admin.ModelAdmin):
    search_fields = ['nume_alergeni']

class BauturiAdmin(admin.ModelAdmin):
    search_fields = ['bautura']

class InghetataAdmin(admin.ModelAdmin):
    search_fields = ['aroma']

class BiscuiteAdmin(admin.ModelAdmin):
    search_fields = ['tip_biscuite']

class TorturiInghetataAdmin(admin.ModelAdmin):
    search_fields = ['nume_tort']

class MeniuAdmin(admin.ModelAdmin):
    search_fields = ['inghetata__aroma', 'biscuiti__tip_biscuite', 'bauturi__bautura']

class InformatiiAdmin(admin.ModelAdmin):
    search_fields = ['descriere']

class SponsorAdmin(admin.ModelAdmin):
    search_fields = ['nume_sponsor']

class MagazineAdmin(admin.ModelAdmin):
    search_fields = ['nume_magazin']

# Inregistrarea modelelor în admin
admin.site.register(Adresa, AdresaAdmin)
admin.site.register(Alergeni, AlergeniAdmin)
admin.site.register(Bauturi, BauturiAdmin)
admin.site.register(Inghetata, InghetataAdmin)
admin.site.register(Biscuite, BiscuiteAdmin)
admin.site.register(Prajituri, PrajituriAdmin)
admin.site.register(Torturi_Inghetata, TorturiInghetataAdmin)
admin.site.register(Meniu, MeniuAdmin)
admin.site.register(Comanda, ComandaAdmin)
admin.site.register(Informatii, InformatiiAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Magazine, MagazineAdmin)
