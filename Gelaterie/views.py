from django.http import HttpResponse
from Gelaterie.models import Adresa, Alergeni, Bauturi, Inghetata, Biscuite, Prajituri, Torturi_Inghetata, Meniu, Comanda, Informatii, Sponsor, Magazine
from django.shortcuts import render

def home(request):
    return HttpResponse("Salut")

def adresa(request):
    adrese_list = Adresa.objects.all()
    response = "<br>".join([
        f"<br>Tara: {adrese.tara}, "
        f"<br>Oras: {adrese.oras}, "
        f"<br>Strada: {adrese.strada}, "
        f"<br>Magazin: {adrese.magazin}"
        for adrese in adrese_list
    ]) 
    return HttpResponse(f"Adresele: <ul>{response}</ul>")

def afiseaza_alergeni(request):
    alergeni = Alergeni.objects.all()
    response = "<br>".join([str(alergen.nume_alergeni) for alergen in alergeni]) 
    return HttpResponse(f"Alergenii disponibili:<br>{response}")

def bauturi(request):
    bauturi_list = Bauturi.objects.all()
    response = "<br>".join([
        f"<br>Băutură: {bautura.bautura}, "
        f"<br>Pret: {bautura.info.pret}, "
        f"<br>Temperatura: {bautura.temperatura}, "
        f"<br>Informatii: {bautura.info.descriere}, Specificatii: {bautura.info.specificatii}"
        for bautura in bauturi_list
    ])
    return HttpResponse(f"Băuturi disponibile:<ul>{response}</ul>")

def inghetata(request):
    inghetata_list = Inghetata.objects.all()
    response = "<br>".join([
        f"<br>Tip inghetata: {inghetate.inghetata}, "
        f"<br>Aroma: {inghetate.aroma}, "
        f"<br>Mod servire: {inghetate.mod_servire}, "
        f"<br>Info: {inghetate.info.descriere}, Specificatii: {inghetate.info.specificatii}, "
        f"<br>Pret: {inghetate.info.pret}"
        for inghetate in inghetata_list
    ])
    return HttpResponse(f"Inghetate disponibile:<ul>{response}</ul>")

def biscuiti(request):
    biscuiti_list = Biscuite.objects.all()
    response = "<br>".join([
        f"<br>Tip biscuite: {biscuite.tip_biscuite}, "
        f"<br>Info: {biscuite.info.descriere}, Specificatii: {biscuite.info.specificatii}, "
        f"<br>Pret: {biscuite.info.pret}"
        for biscuite in biscuiti_list
    ])
    return HttpResponse(f"Biscuiti disponibili:<ul>{response}</ul>")

def prajituri(request):
    prajituri_list = Prajituri.objects.all()
    response = "<br>".join([
        f"<br>Prajitura: {prajitura.nume_prajitura}, "
        f"<br>Info: {prajitura.info.descriere}, Specificatii: {prajitura.info.specificatii}, "
        f"<br>Pret: {prajitura.info.pret}"
        for prajitura in prajituri_list
    ])
    return HttpResponse(f"Prajituri disponibile:<ul>{response}</ul>")

def torturi_inghetata(request):
    torturi_list = Torturi_Inghetata.objects.all()
    response = "<br>".join([
        f"<br>Tort: {tort.nume_tort}, "
        f"<br.Info: {tort.info.descriere}, Specificatii: {tort.info.specificatii}, "
        f"<br>Pret: {tort.info.pret}"
        for tort in torturi_list
    ])
    return HttpResponse(f"Torturi inghetata disponibile:<ul>{response}</ul>")

def meniu(request):
    meniu_list = Meniu.objects.all()
    response = "<br>".join([
        f"<br>Inghetata: {meniu.inghetata.aroma}, "
        f"<br>Biscuiti: {meniu.biscuiti.tip_biscuite}, "
        f"<br>Bauturi: {meniu.bauturi.bautura}, "
        f"<br>Prajituri: {meniu.prajituri.nume_prajitura}, "
        f"<br>Torturi: {meniu.torturi_inghetata.nume_tort}"
        for meniu in meniu_list
    ])
    return HttpResponse(f"Meniu:<ul>{response}</ul>")

def comenzi(request):
    comenzi_list = Comanda.objects.all()
    response = "<br>".join([
        f"<br>Data achizitie: {comanda.data_achizitie}, "
        f"<br>Livrare curier: {'Da' if comanda.livrare_curier else 'Nu'}, "
        f"<br>Informatii: {', '.join([info.specificatii for info in comanda.informatii.all()])}"
        for comanda in comenzi_list
    ])
    return HttpResponse(f"Comenzi:<ul>{response}</ul>")

def sponsori(request):
    sponsori_list = Sponsor.objects.all()
    response = "<br>".join([
        f"<br>Nume: {sponsor.nume_sponsor}, "
        f"<br>Email: {sponsor.email_sponsor}, "
        f"<br>Telefon: {sponsor.numar_telefon_sponsor}"
        for sponsor in sponsori_list
    ])
    return HttpResponse(f"Sponsori:<ul>{response}</ul>")

def magazine(request):
    magazine_list = Magazine.objects.all()
    response = "<br>".join([
        f"<br>Nume magazin: {magazin.nume_magazin}, "
        f"<br>Descriere: {magazin.descriere}, "
        f"<br>Orar: {magazin.orar}, "
        f"<br>Email: {magazin.email_magazin}, "
        f"<br>Telefon: {magazin.numar_telefon_magazin}, "
        f"<br>Sponsor: {magazin.sponsor.nume_sponsor}"
        for magazin in magazine_list
    ])
    return HttpResponse(f"Magazine:<ul>{response}</ul>")

def informatii(request):
    informatii_list = Informatii.objects.all()
    response = "<br>".join([
        f"<br>Specificatii: {info.specificatii}, "
        f"<br>Descriere: {info.descriere}, "
        f"<br>Pret: {info.pret}, "
        f"<br>Alergeni: {', '.join([alergen.nume_alergeni for alergen in info.alergeni.all()])}"
        for info in informatii_list
    ])
    return HttpResponse(f"Informatii disponibile:<ul>{response}</ul>")



def display_items(request):
    return render(request, 'store.html')
