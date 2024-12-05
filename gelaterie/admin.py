from django.contrib import admin
from .models import (
    Adresa, Alergeni, Bauturi, Inghetata, Biscuite, Prajituri, 
    Torturi_Inghetata, Meniu, Comanda, Informatii, Sponsor, Magazine, CustomUser,  Vizualizare, Promotie
)

from django.contrib.auth.admin import UserAdmin


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


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'telefon', 'adresa', 'age', 'first_name', 'last_name',
        'sex', 'nationalitate', 'cod', 'email_confirmat', 'is_staff', 'is_blocked'
    )
    search_fields = (
        'username', 'email', 'telefon', 'adresa',
        'nationalitate'
    )
    list_filter = ('is_staff', 'is_active', 'is_blocked')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informații personale', {'fields': (
            'first_name',  
            'last_name',   
            'email',      
            'telefon',    
            'adresa',     
            'age',         
            'sex',        
            'nationalitate',
            'cod',         
            'email_confirmat'  
        )}),
        ('Blocare utilizator', {'fields': ('is_blocked',)}),  
        ('Permisiuni', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Date importante', {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        
        if not request.user.is_superuser and request.user.groups.filter(name="Moderatori").exists():
            # Campurile astea nu le poate accesa un Moderator, doar vedea
            readonly_fields += (
                'username',
                'telefon',
                'adresa',
                'age',
                'sex',
                'nationalitate',
                'cod',
                'email_confirmat',
                'is_staff',
                'groups',
                'user_permissions'
            )

        return readonly_fields




class VizualizareAdmin(admin.ModelAdmin):
    list_display = ('utilizator', 'produs', 'categorie', 'data_vizualizare')  
    search_fields = ('utilizator__username', 'produs__specificatii')  
    list_filter = ('data_vizualizare', 'categorie') 
    ordering = ('-data_vizualizare',)  


class PromotieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'data_creare', 'data_expirare', 'categorie', 'discount') 
    search_fields = ('nume', 'categorie')  
    list_filter = ('data_creare', 'data_expirare', 'categorie') 
    ordering = ('-data_creare',) 




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
admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Vizualizare, VizualizareAdmin)
admin.site.register(Promotie, PromotieAdmin)