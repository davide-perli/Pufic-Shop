from django.http import HttpResponse
from gelaterie.models import Adresa, Alergeni, Bauturi, Inghetata, Biscuite, Prajituri, Torturi_Inghetata, Meniu, Comanda, Informatii, Sponsor, Magazine
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import PrajituriFilterForm
from .forms import ContactForm
import time, os, json
from datetime import date, datetime
from .forms import ComandaForm
from .models import Informatii
import decimal
from django.contrib.auth import login
from .forms import CustomAuthenticationForm     

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
        f"<br>Pret: {bautura.info.pret if bautura.info else 'N/A'}, "
        f"<br>Temperatura: {bautura.temperatura}, "
        f"<br>Informatii: {bautura.info.descriere if bautura.info else 'N/A'}, Specificatii: {bautura.info.specificatii if bautura.info else 'N/A'}"
        for bautura in bauturi_list
    ])
    return HttpResponse(f"Băuturi disponibile:<ul>{response}</ul>")

def inghetata(request):
    inghetata_list = Inghetata.objects.all()
    response = "<br>".join([
        f"<br>Tip inghetata: {inghetate.inghetata}, "
        f"<br>Aroma: {inghetate.aroma}, "
        f"<br>Mod servire: {inghetate.mod_servire}, "
        f"<br>Info: {inghetate.info.descriere if inghetate.info else 'N/A'}, Specificatii: {inghetate.info.specificatii if inghetate.info else 'N/A'}, "
        f"<br>Pret: {inghetate.info.pret if inghetate.info else 'N/A'}"
        for inghetate in inghetata_list
    ])
    return HttpResponse(f"Inghetate disponibile:<ul>{response}</ul>")

def biscuiti(request):
    biscuiti_list = Biscuite.objects.all()
    response = "<br>".join([
        f"<br>Tip biscuite: {biscuite.tip_biscuite}, "
        f"<br>Info: {biscuite.info.descriere if biscuite.info else 'N/A'}, Specificatii: {biscuite.info.specificatii if biscuite.info else 'N/A'}, "
        f"<br>Pret: {biscuite.info.pret if biscuite.info else 'N/A'}"
        for biscuite in biscuiti_list
    ])
    return HttpResponse(f"Biscuiti disponibili:<ul>{response}</ul>")

def prajituri(request):
    prajituri_list = Prajituri.objects.all()
    response = "<br>".join([
        f"<br>Prajitura: {prajitura.nume_prajitura}, "
        f"<br>Info: {prajitura.info.descriere if prajitura.info else 'N/A'}, Specificatii: {prajitura.info.specificatii if prajitura.info else 'N/A'}, "
        f"<br>Pret: {prajitura.info.pret if prajitura.info else 'N/A'}"
        for prajitura in prajituri_list
    ])
    return HttpResponse(f"Prajituri disponibile:<ul>{response}</ul>")


def torturi_inghetata(request):
    torturi_list = Torturi_Inghetata.objects.all()
    response = "<br>".join([
        f"<br>Tort: {tort.nume_tort}, "
        f"<br>Info: {tort.info.descriere}, Specificatii: {tort.info.specificatii}, "
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

    inghetata_items = Inghetata.objects.all()
    bauturi_items = Bauturi.objects.all()
    biscuiti_items = Biscuite.objects.all()
    prajituri_items = Prajituri.objects.all().order_by('info__pret') #Schimbati ordinea afisarii campurilor pentru minim unul dintre modele
    torturi_items = Torturi_Inghetata.objects.all()
    meniu_items = Meniu.objects.all()
    sponsors = Sponsor.objects.all()

    context = {
        'inghetata_items': inghetata_items,
        'bauturi_items': bauturi_items,
        'biscuiti_items': biscuiti_items,
        'prajituri_items': prajituri_items,
        'torturi_items': torturi_items,
        'meniu_items': meniu_items,
        'sponsors': sponsors,
    }

    return render(request, 'store.html', context)

def display_products(request):

    form = PrajituriFilterForm(request.GET or None)

    prajituri = Prajituri.objects.all()

    if form.is_valid():
        nume = form.cleaned_data.get('nume')
        pret_min = form.cleaned_data.get('pret_min')
        pret_max = form.cleaned_data.get('pret_max')
        magazin_disponibil = form.cleaned_data.get('magazin_disponibil')
        alergeni_in = form.cleaned_data.get('alergeni_in')

        # Aplicare filtre
        if nume:
            prajituri = prajituri.filter(nume_prajitura__icontains = nume)
        if pret_min is not None:
            prajituri = prajituri.filter(info__pret__gte = pret_min)
        if pret_max is not None:    
            prajituri = prajituri.filter(info__pret__lte = pret_max)
        if magazin_disponibil:
            prajituri = prajituri.filter(magazin__nume_magazin__icontains = magazin_disponibil)
        if alergeni_in:
            prajituri = prajituri.filter(info__alergeni__nume_alergeni__icontains = alergeni_in)

    # Paginarea: 5 prajituri pe pagina
    paginator = Paginator(prajituri, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'display_products.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            data_nasterii = cleaned_data['data_nasterii']
            today = date.today()
            ani = today.year - data_nasterii.year

            mesaj = ' '.join(cleaned_data['mesaj'].split()) 

            data_to_save = {
                "nume": cleaned_data['nume'],
                "prenume": cleaned_data['prenume'],
                "varsta": f"{ani} ani",
                "email": cleaned_data['email'],
                "confirm_email" : cleaned_data['confirm_email'],
                "tip_mesaj": cleaned_data['tip_mesaj'],
                "subiect": cleaned_data['subiect'],
                "zile_asteptare": cleaned_data['zile_asteptare'],
                "mesaj": cleaned_data['mesaj']
            }

            folder_path = os.path.join(os.getcwd(), 'mesaje') # Path folder

            # Salvare data in json
            timestamp = int(time.time())
            file_name = f"mesaj_{timestamp}.json"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as json_file:
                json.dump(data_to_save, json_file, indent=4)

            return redirect('mesaj_trimis')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def mesaj_trimis(request):
    return render(request, 'mesaj_trimis.html', {'message': 'Mesajul tău a fost trimis cu succes!'})



def adauga_comanda(request):
    if request.method == 'POST':
        form = ComandaForm(request.POST)
        if form.is_valid():
            # Preluare obiect fara salvare
            comanda = form.save(commit=False)

            # Procesez campurile adaugate
            cos_cumparaturi = form.cleaned_data['cos_cumparaturi']
            note = form.cleaned_data.get('note', '')
            discount_procent = form.cleaned_data.get('discount_procent', 0)

            # Aplic discount
            if discount_procent:
                discount = decimal.Decimal(discount_procent) / 100
                for info in form.cleaned_data['informatii']:
                    pret_reduse = info.pret * (1 - discount)
                    info.pret = round(pret_reduse, 2)
                    info.save()

            # Setare info extra in comanda
            comanda.note = note
            comanda.cos_cumparaturi = cos_cumparaturi

            # Save comanda (campurile extra nu vor fi ca doar sunt extra si nu le-am definit in model)
            comanda.save()
            form.save_m2m()  # Save relatiile many-to-many

            return redirect('mesaj_trimis') 
    else:
        form = ComandaForm()

    return render(request, 'adauga_comanda.html', {'form': form})




def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get('ramane_logat'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2*7*24*60*60)  # 2 săptămâni în secunde            
            return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})
