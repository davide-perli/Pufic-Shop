from django.db import models
from django.utils import timezone
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
    alergeni = models.ManyToManyField(Alergeni)


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