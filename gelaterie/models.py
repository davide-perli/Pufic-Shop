from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import random
import string
from django.utils.timezone import now

import json
import os
from django.conf import settings


#1
class Sponsor(models.Model):
    nume_sponsor = models.CharField(max_length = 100)
    email_sponsor = models.EmailField(null = True)
    numar_telefon_sponsor = models.BigIntegerField(null = True)

#2
class Magazine(models.Model):
    id = models.SmallIntegerField(primary_key = True, null = False)
    nume_magazin = models.CharField(max_length = 50)
    descriere = models.TextField(null=True, blank=True)
    orar = models.DateField(null = True)
    email_magazin = models.EmailField(null = True)
    numar_telefon_magazin = models.BigIntegerField(null = True)
    sponsor = models.ForeignKey(Sponsor, on_delete = models.CASCADE) # Relatie many to one

#3
class Adresa(models.Model):
    tara = models.CharField(max_length = 50)
    oras = models.CharField(max_length = 50)
    strada = models.CharField(max_length = 150)
    magazin = models.OneToOneField(Magazine, on_delete=models.CASCADE, null = True)  # Relatie one to one

#4
class Alergeni(models.Model):
    optiuni_alergeni = (
        ("LACTOZA", "lactoza"),
        ("GLUTEN", "gluten"),
        ("ALUNE", "alune"),
        ("NONE", "none"),
    )
    nume_alergeni = models.CharField(choices = optiuni_alergeni, default = "NONE")

#5
class Informatii(models.Model):
    specificatii = models.CharField(max_length = 250, blank = True)
    descriere = models.TextField(null=True, blank=True)
    pret = models.DecimalField(max_digits = 5, decimal_places = 2, null = True)
    stoc = models.IntegerField(default = 10)
    alergeni = models.ManyToManyField(Alergeni)

    def __str__(self):
        return f"{self.specificatii} - {self.pret} RON"


#6
class Inghetata(models.Model):
    optiuni_inghetata = (
        ("GELATO", "gelato"),
        ("SORBET", "sorbet")
    )
    optiuni_servire = (
        ("CON", "con"),
        ("CUPA", "cupa")
    )
    optiuni_aroma = (
        ("CIOCOLATA", "ciocolata"),
        ("CIOCOLATA ALBA", "ciocolata alba"),
        ("VANILIE", "vanilie"),
        ("FISTIC", "fistic"),
        ("COOKIES ADN CREAM", "cookies and cream"),
        ("CARAMEL", "caramel"),
        ("KINDER", "kinder"),
        ("BUBBLEGUM", "bubblegum"),
        ("ALUNE", "alune"),
        ("CASTANE", "castane"),
        ("PEPENE", "pepene"),
        ("BANANA", "banana"),
        ("CIRESE", "cirese"),
        ("PIERSICI", "piersici"),
        ("LAMAIE", "lamaie")
    )
    inghetata = models.CharField(choices = optiuni_inghetata, default = "GELATO")
    aroma =  models.CharField(choices = optiuni_aroma, default = "CIOCOLATA")
    mod_servire = models.CharField(choices = optiuni_servire, default = "CON")
    info = models.OneToOneField(Informatii, on_delete = models.CASCADE, null = True, blank = True) # Relatie one to one
    magazin = models.ManyToManyField(Magazine)

#7
class Biscuite(models.Model):
    optiuni_biscuiti = (
        ("CIOCOLATA", "ciocolata"),
        ("CIOCOLATA ALBA", "ciocolata alba"),
        ("GRAHAM", "graham"),
        ("DIGESTIVI", "digestivi"),
        ("UNT", "unt")
    )
    info = models.OneToOneField(Informatii, on_delete = models.CASCADE, null = True, blank = True) # Relatie one to one
    tip_biscuite = models.CharField(choices = optiuni_biscuiti, default = "CIOCOLATA")
    magazin = models.ManyToManyField(Magazine)


#8
class Bauturi(models.Model):
    optiuni_temperatura = (
        ("RECE", "rece"),
        ("CAMEREI", "camerei"),
        ("CALDA", "calda")
    )
    optiuni_bauturi = (
        ("CAFEA", "cafea"),
        ("CEAI", "ceai"),
        ("LAPTE", "lapte"),
        ("MILKSHAKE", "milkshake"),
        ("COCA-COLA", "coca-cola"),
        ("PEPSI", "pepsi"),
        ("FANTA", "fanta"),
        ("LIPTON", "lipton"),
    )
    bautura = models.CharField(choices = optiuni_bauturi, default = "CAFEA")
    info = models.OneToOneField(Informatii, on_delete = models.CASCADE, null = True, blank = True) # Relatie one to one
    temperatura = models.CharField(choices = optiuni_temperatura, default = "CAMEREI")
    magazin = models.ManyToManyField(Magazine)

#9
class Prajituri(models.Model):
    optiuni_prajituri = (
        ("MOUSSE", "mousse"),
        ("LAVACAKE", "lavacake"),
        ("PROFITEROL", "profiterol"),
        ("TARTE FRUCTE", "tarte fructe"),
        ("CREME BRULEE", "creme brulee"),
        ("ECLAIR", "eclair"),
        ("MACAROONS", "macaroons"),
        ("RED VELVET", "red velvet"),
    )
    nume_prajitura = models.CharField(choices = optiuni_prajituri, default = "MOUSSE")
    info = models.OneToOneField(Informatii, on_delete = models.CASCADE, null = True, blank = True) # Relatie one to one
    magazin = models.ManyToManyField(Magazine)

#10
class Torturi_Inghetata(models.Model):
    optiuni_torturi = (
        ("MOUSSE", "mousse"),
        ("SACHER", "sacher"),
        ("RED VELVET", "red velvet"),
        ("BLACK FOREST", "black forest"),
    )
    nume_tort = models.CharField(choices = optiuni_torturi, default = "MOUSSE")
    info = models.OneToOneField(Informatii, on_delete = models.CASCADE, null = True, blank = True) # Relatie one to one
    magazin = models.ManyToManyField(Magazine)

#11
class Meniu(models.Model):
    inghetata = models.ForeignKey(Inghetata, on_delete = models.CASCADE, null = True)                 # Relatie many to one
    biscuiti = models.ForeignKey(Biscuite, on_delete = models.CASCADE, null = True)                   # Relatie many to one
    bauturi = models.ForeignKey(Bauturi, on_delete = models.CASCADE, null = True)                     # Relatie many to one
    prajituri = models.ForeignKey(Prajituri, on_delete = models.CASCADE, null = True)                 # Relatie many to one
    torturi_inghetata = models.ForeignKey(Torturi_Inghetata, on_delete = models.CASCADE, null = True) # Relatie many to one
    
    
#12
class Comanda(models.Model):
    data_achizitie = models.DateField(default = timezone.now)
    livrare_curier = models.BooleanField(default = True)
    informatii = models.ManyToManyField(Informatii, blank = True)


#13
class CustomUser(AbstractUser):
    optiuni_sex = (
        ("BARBAT", "barbat"),
        ("FEMEIE", "femeie"),
        ("NONE", "none"),
    )
    telefon = models.CharField(max_length = 15, blank = True)
    adresa = models.CharField(max_length = 150, blank = True)
    age = models.SmallIntegerField(null = True)
    sex = models.CharField(choices = optiuni_sex, default = "NONE")
    nationalitate = models.CharField(max_length = 50, blank = True)
    cod = models.CharField(max_length = 100, blank = True)
    email_confirmat = models.BooleanField(default = False)
    is_blocked = models.BooleanField(default = False)


    def generate_cod(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def save(self, *args, **kwargs):
        if not self.cod:
            self.cod = self.generate_cod()
        super().save(*args, **kwargs)


        # Salvare parola intr-un fisier JSON
        if hasattr(self, 'raw_password'):
            user_data = {
                "username": self.username,
                "password": self.raw_password,  # Aribut temporar pentru parola necriptata
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "ip_address": self.ip_address,
                "browser_info": self.browser_info,
        }
            username = self.username
            password_dir = os.path.join(settings.BASE_DIR, 'user_data')

            # Creare folder daca nu exista
            if not os.path.exists(password_dir):
                os.makedirs(password_dir)

            # Salvare parola in fiser json
            password_file_path = os.path.join(password_dir, f"{username}.json")
            with open(password_file_path, 'w') as json_file:
                json_file.write("[\n")
                json.dump({"username": self.username}, json_file)
                json_file.write(",\n") 
                json.dump({"password" : self.raw_password}, json_file)
                json_file.write(",\n")
                json.dump({"first_name": self.first_name}, json_file)
                json_file.write(",\n")  
                json.dump({"last_name": self.last_name}, json_file)
                json_file.write(",\n") 
                json.dump({"email": self.email}, json_file)
                json_file.write(",\n") 
                json.dump({"ip_address": self.ip_address}, json_file)
                json_file.write(",\n")  
                json.dump({"browser_info": self.browser_info}, json_file)
                json_file.write(",\n") 
                json.dump({"telefon": self.telefon}, json_file)
                json_file.write(",\n")
                json.dump({"adresa": self.adresa}, json_file)
                json_file.write(",\n")
                json.dump({"age": self.age}, json_file)
                json_file.write(",\n")
                json.dump({"sex": self.sex}, json_file)
                json_file.write(",\n")
                json.dump({"location_city": self.location_city}, json_file)
                json_file.write(",\n")
                json.dump({"location_region": self.location_region}, json_file)
                json_file.write(",\n")
                json.dump({"location_country": self.location_country}, json_file)
                json_file.write("\n]") 

    class Meta:
        permissions = [
            ("vizualizeaza_oferta", "Permite vizualizarea ofertei"),
        ]
        



#14
class Vizualizare(models.Model):
    utilizator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    produs = models.ForeignKey(Informatii, on_delete=models.CASCADE, null=True, blank=True)
    categorie = models.CharField(max_length=100, null=True, blank=True)  # Nou câmp
    data_vizualizare = models.DateTimeField(default=now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['utilizator', 'categorie'], name='unique_vizualizare_per_utilizator_categorie')
        ]

#15
class Promotie(models.Model):
    nume = models.CharField(max_length = 100)
    data_creare = models.DateTimeField(auto_now_add = True)
    data_expirare = models.DateTimeField()
    categorie = models.CharField(max_length = 100)
    descriere = models.TextField()
    discount = models.DecimalField(max_digits = 5, decimal_places=2)

    def __str__(self):
        return f"{self.nume} - Expira: {self.data_expirare}"
    
