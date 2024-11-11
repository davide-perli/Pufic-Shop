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

# Impartirea campurilor in sectiuni pentru Comanda
class ComandaAdmin(admin.ModelAdmin):
    search_fields = ['data_achizitie']
    list_filter = ['data_achizitie']
    fieldsets = (
        ("Informații Generale", {
            'fields': ('data_achizitie', 'livrare_curier')
        }),
        ("Detalii Produs", {
            'fields': ('informatii',),
            'classes': ('collapse',), #sectiune pliabila
        }),
    )

class AdresaAdmin(admin.ModelAdmin):
    search_fields = ['tara', 'oras']
    list_filter = ['tara', 'oras'] 

class AlergeniAdmin(admin.ModelAdmin):
    search_fields = ['nume_alergeni']
    list_filter = ['nume_alergeni']

class BauturiAdmin(admin.ModelAdmin):
    search_fields = ['bautura']
    list_filter = ['bautura']

class InghetataAdmin(admin.ModelAdmin):
    search_fields = ['aroma']
    list_filter = ['aroma']

class BiscuiteAdmin(admin.ModelAdmin):
    search_fields = ['tip_biscuite']
    list_filter = ['tip_biscuite']

class TorturiInghetataAdmin(admin.ModelAdmin):
    search_fields = ['nume_tort']
    list_filter = ['nume_tort']

class MeniuAdmin(admin.ModelAdmin):
    search_fields = ['inghetata__aroma', 'biscuiti__tip_biscuite', 'bauturi__bautura']
    list_filter = ['inghetata__aroma', 'biscuiti__tip_biscuite', 'bauturi__bautura']

class InformatiiAdmin(admin.ModelAdmin):
    search_fields = ['descriere']
    list_filter = ['descriere']

class SponsorAdmin(admin.ModelAdmin):
    search_fields = ['nume_sponsor']
    list_filter = ['nume_sponsor']

class MagazineAdmin(admin.ModelAdmin):
    search_fields = ['nume_magazin']
    list_filter = ['nume_magazin']

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
