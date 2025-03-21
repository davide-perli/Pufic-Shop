from django.http import HttpResponse
from gelaterie.models import Adresa, Alergeni, Bauturi, Inghetata, Biscuite, Prajituri, Torturi_Inghetata, Meniu, Comanda, Informatii, Sponsor, Magazine, Promotie, Vizualizare
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import PrajituriFilterForm
from .forms import ContactForm
import time, os, json
from datetime import date
from .forms import ComandaForm
from .models import Informatii
from decimal import Decimal
from django.contrib.auth import login
from .forms import CustomAuthenticationForm    
from .forms import CustomUserCreationForm
from django.contrib.auth import logout 
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser
from datetime import datetime

import random
import string


from django.core.mail import send_mass_mail
from .models import  Vizualizare
from django.utils.timezone import now
from .forms import PromotieForm
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test

from django.core.mail import EmailMultiAlternatives
from .forms import PrajituriForm

from django.http import JsonResponse

from django.contrib import messages

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from gelaterie.models import CustomUser

import requests

import logging


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.core.mail import EmailMessage


logger = logging.getLogger('django')

def home(request):
    logger.info("--------------Functia home a fost apelata")
    return HttpResponse("Salut")

def adresa(request):
    logger.info("--------------Functia adresa a fost apelata")

    if request.user.username != 'davide':
        mesaj_personalizat = "Accesul la informatiile despre adrese este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze adresele fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    adrese_list = Adresa.objects.all()
    response = "<br>".join([f"<br>Tara: {adrese.tara}, <br>Oras: {adrese.oras}, <br>Strada: {adrese.strada}, <br>Magazin: {adrese.magazin.nume_magazin}" for adrese in adrese_list])
    logger.debug("--------------Adresele au fost extrase cu succes!")
    return HttpResponse(f"Adresele: <ul>{response}</ul>")

def afiseaza_alergeni(request):
    logger.info("--------------Functia afisare_alergeni a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre alergeni este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze alergenii fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    alergeni = Alergeni.objects.all()
    response = "<br>".join([str(alergen.nume_alergeni) for alergen in alergeni])
    logger.debug("--------------Alergenii au fost extrasi cu succes!")
    return HttpResponse(f"Alergenii disponibili:<br>{response}")

def bauturi(request):
    logger.info("--------------Functia bauturi a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre bauturi este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze bauturile fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    bauturi_list = Bauturi.objects.all()
    response = "<br>".join([f"<br>Bautura: {bautura.bautura}, <br>Pret: {bautura.info.pret if bautura.info else 'N/A'}, <br>Temperatura: {bautura.temperatura}, <br>Informatii: {bautura.info.descriere if bautura.info else 'N/A'}, Specificatii: {bautura.info.specificatii if bautura.info else 'N/A'}" for bautura in bauturi_list])
    logger.debug("--------------Bauturile au fost extrase cu succes!")
    return HttpResponse(f"Băuturi disponibile:<ul>{response}</ul>")

def inghetata(request):
    logger.info("--------------Functia inghetata a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre inghetate este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze inghetatele fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    inghetata_list = Inghetata.objects.all()
    response = "<br>".join([f"<br>Tip inghetata: {inghetate.inghetata}, <br>Aroma: {inghetate.aroma}, <br>Mod servire: {inghetate.mod_servire}, <br>Info: {inghetate.info.descriere if inghetate.info else 'N/A'}, Specificatii: {inghetate.info.specificatii if inghetate.info else 'N/A'}, <br>Pret: {inghetate.info.pret if inghetate.info else 'N/A'}" for inghetate in inghetata_list])
    logger.debug("--------------Inghetatele au fost extrase cu succes!")
    return HttpResponse(f"Inghetate disponibile:<ul>{response}</ul>")

def biscuiti(request):
    logger.info("--------------Functia biscuiti a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre biscuiti este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze biscuitii fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    biscuiti_list = Biscuite.objects.all()
    response = "<br>".join([f"<br>Tip biscuite: {biscuite.tip_biscuite}, <br>Info: {biscuite.info.descriere if biscuite.info else 'N/A'}, Specificatii: {biscuite.info.specificatii if biscuite.info else 'N/A'}, <br>Pret: {biscuite.info.pret if biscuite.info else 'N/A'}" for biscuite in biscuiti_list])
    logger.debug("--------------Biscuitii au fost extrasi cu succes!")
    return HttpResponse(f"Biscuiti disponibili:<ul>{response}</ul>")

def prajituri(request):
    logger.info("--------------Functia prajituri a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre prajituri este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze prajiturile fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    prajituri_list = Prajituri.objects.all()
    response = "<br>".join([f"<br>Prajitura: {prajitura.nume_prajitura}, <br>Info: {prajitura.info.descriere if prajitura.info else 'N/A'}, Specificatii: {prajitura.info.specificatii if prajitura.info else 'N/A'}, <br>Pret: {prajitura.info.pret if prajitura.info else 'N/A'}" for prajitura in prajituri_list])
    logger.debug("--------------Prajiturile au fost extrase cu succes!")
    return HttpResponse(f"Prajituri disponibile:<ul>{response}</ul>")


def torturi_inghetata(request):
    logger.info("--------------Functia torturi_inghetata a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre torturile de ingheata este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze torturile de inghetata fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    torturi_list = Torturi_Inghetata.objects.all()
    response = "<br>".join([f"<br>Tort: {tort.nume_tort}, <br>Info: {tort.info.descriere}, Specificatii: {tort.info.specificatii}, <br>Pret: {tort.info.pret}" for tort in torturi_list])
    logger.debug("--------------Torturile de inghetata au fost extrase cu succes!")
    return HttpResponse(f"Torturi inghetata disponibile:<ul>{response}</ul>")

def meniu(request):
    logger.info("--------------Functia meniu a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre meniu este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze meniul fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    meniu_list = Meniu.objects.all()
    response = "<br>".join([f"<br>Inghetata: {meniu.inghetata.aroma}, "
                            f"<br>Biscuiti: {meniu.biscuiti.tip_biscuite}, "
                            f"<br>Bauturi: {meniu.bauturi.bautura}, "
                            f"<br>Prajituri: {meniu.prajituri.nume_prajitura}, "
                            f"<br>Torturi: {meniu.torturi_inghetata.nume_tort}" for meniu in meniu_list])
    logger.debug("--------------Meniurile au fost extrase cu succes!")
    return HttpResponse(f"Meniu:<ul>{response}</ul>")

def comenzi(request):
    logger.info("--------------Functia comenzi a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre comenzi este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze comenzile fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': "Acces Interzis",
            "mesaj_personalizat": mesaj_personalizat,
            "user": request.user,
        }, status=403)

    try:
        comenzi_list = Comanda.objects.all()
        response = "<br>".join([f"<br>Data achizitie: {comanda.data_achizitie}" for comanda in comenzi_list])
        
        logger.debug("--------------Comenzile au fost extrase cu succes!")
        return HttpResponse(f"Comenzi:<ul>{response}</ul>")
        
    except Exception as e:
        logger.error("Eroare la extragerea comenzilor: %s", str(e))
        
        return HttpResponse("A aparut o eroare la extragerea comenzilor!")

def sponsori(request):
    logger.info("--------------Functia sponsori a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre sponsori este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else ''} a incercat să acceseze sponsorii fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, "403.html", {
            "title": "Acces Interzis",
            "mesaj_personalizat": mesaj_personalizat,
            "user": request.user,
        }, status=403)

    sponsori_list = Sponsor.objects.all()

    response = "<br>".join([
        f"<br>Nume sponsor: {sponsor.nume_sponsor}, "
        f"<br>Email sponsor: {sponsor.email_sponsor}"
        for sponsor in sponsori_list
    ])
    logger.debug("--------------Sponsorii au fost extrasi cu succes!")
    return HttpResponse(f"Sponsori:<ul>{response}</ul>")


def magazine(request):
   logger.info("--------------Functia magazine a fost apelata")

   if not request.user.is_superuser:
       mesaj_personalizat = "Accesul la informatiile despre magazine este restrictionat!"
       logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else ''} a incercat sa acceseze magazinele fara permisiune!")
       messages.warning(request, "Acesta este un avertisment. :| ")
       messages.error(request, "A aparut o eroare! >:((  ")
       return render(request, "403.html", {
           "title": "Acces Interzis",
           "mesaj_personalizat": mesaj_personalizat,
           "user": request.user,
       }, status=403)

   magazine_list = Magazine.objects.all()
   response = "<br>".join([
       f"<br>Nume magazin:{magazin.nume_magazin}, "
       f"<br>Email:{magazin.email_magazin}"
       for magazin in magazine_list])
   logger.debug("--------------Magazinele au fost extrase cu succes!")
   return HttpResponse(f"Magazine:<ul>{response}</ul>")


def informatii(request):
    logger.info("--------------Functia informatii a fost apelata")

    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre produse este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze informatiile fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)


    informatii_list = Informatii.objects.all()
    response = "<br>".join([f"<br>Specificatii: {info.specificatii}, "
                            f"<br>Descriere: {info.descriere}, "
                            f"<br>Pret: {info.pret}, "
                            f"<br>Stoc: {info.stoc}, "
                            f"<br>Alergeni: {', '.join([alergen.nume_alergeni for alergen in info.alergeni.all()])}"
                            for info in informatii_list])

    logger.info("--------------Informatiile au fost extrase cu succes")
    return HttpResponse(f"Informatii disponibile:<ul>{response}</ul>")


def display_items(request):
    logger.info("--------------Functia display_items a fost apelata")
    inghetata_items = Inghetata.objects.all()
    bauturi_items = Bauturi.objects.all().order_by('info__pret')
    biscuiti_items = Biscuite.objects.all().order_by('info__pret')
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
    
    logger.debug("--------------Functia display_items executata cu succes!")
    return render(request, 'store.html', context)

def display_products(request):
    logger.info("--------------Functia display_products a fost apelata")
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
    logger.debug("--------------Functia display_products executata cu succes!")
    return render(request, 'display_products.html', context)


def contact_view(request):
    logger.info("--------------Functia contact_view a fost apelata")
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            logger.debug("Formularul de contact este valid")

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

            os.makedirs(folder_path, exist_ok=True)

            # Salvare data in json
            timestamp = int(time.time())
            file_name = f"mesaj_{timestamp}.json"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as json_file:
                json.dump(data_to_save, json_file, indent=4)

            return redirect('mesaj_trimis')
    else:
        form = ContactForm()

    logger.debug("--------------Functia contact_view executata cu succes!")
    return render(request, 'contact.html', {'form': form})


def mesaj_trimis(request):
    logger.info("--------------Functia mesaj_trimis a fost apelata")
    return render(request, 'mesaj_trimis.html', {'message': 'Mesajul tau a fost trimis cu succes!'})

def cod_confirmare(request):
    logger.info("--------------Functia cod_confirmare a fost apelata")
    return render(request, 'cod_confirmare.html')

@login_required(login_url='custom_login_view')  
def adauga_comanda(request):
    logger.info("--------------Functia adauga_comanda a fost apelata")
    inghetata_items = Inghetata.objects.all()
    bauturi_items = Bauturi.objects.all()
    biscuiti_items = Biscuite.objects.all()
    prajituri_items = Prajituri.objects.all()
    torturi_items = Torturi_Inghetata.objects.all()
    informatii_items = Informatii.objects.all()

    if request.method == 'POST':
        form = ComandaForm(request.POST)
        if form.is_valid():

            comanda_data = {
                'note': form.cleaned_data.get('note', ''),
                'cos_cumparaturi': form.cleaned_data.get('cos_cumparaturi'),
                
            }
            request.session['comanda_data'] = comanda_data 
            return redirect('comanda_salvare')
    else:
        form = ComandaForm()

    context = {
        'form': form,
        'inghetata_items': inghetata_items,
        'bauturi_items': bauturi_items,
        'biscuiti_items': biscuiti_items,
        'prajituri_items': prajituri_items,
        'torturi_items': torturi_items,
        'informatii': informatii_items,
    }

    messages.debug(request, "Acesta este un mesaj de depanare!!!")
    logger.debug("--------------Functia adauga_comanda executata cu succes!")
    return render(request, 'adauga_comanda.html', context)




def comanda_salvare(request):
    logger.info("--------------Functia comanda_salvare a fost apelata")

    if request.method == 'POST':
        comanda_data = json.loads(request.POST.get('cos_cumparaturi', '[]'))

        if not comanda_data:
            messages.error(request, "Cosul de cumparaturi este gol!")
            return render(request, 'comanda.html')

    
        utilizator = request.user
        comanda = Comanda.objects.create(
            data_achizitie=timezone.now(),
            livrare_curier=True,
        )
        comanda.save()

        total_price = 0
        for item in comanda_data:
            try:
                informatii = Informatii.objects.get(id=item['id'])
                quantity = item['cantitate']
                total_price += informatii.pret * quantity
                comanda.informatii.add(informatii)
            except Informatii.DoesNotExist:
                logger.warning(f"Produsul cu id {item['id']} nu exista.")

        comanda.save()

        # Generare PDF
        factura_pdf = genereaza_factura_pdf(utilizator, comanda, total_price, comanda_data)

        # Trimite email cu factura
        send_invoice_email(utilizator, factura_pdf)

        # Golire cos virtual
        request.session.pop('comanda_data', None)
        messages.success(request, "Comanda a fost realizata cu succes!")

        return redirect('mesaj_trimis')

    messages.warning(request, "Nu s-a trimis nici o comanda!")
    return render(request, 'comanda.html')







def get_site_url(request=None):
    logger.info("--------------Functia get_site_url a fost apelata")
    if request:
        # Daca exista un request, determin automat host-ul
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        return f"{scheme}://{host}"
    # Implicit varianta pentru IP
    logger.debug("--------------Functia get_site_url executata cu succes!")
    return "http://192.168.0.103:8000"


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip", "")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching public IP: {e}")
        return ""


def get_location(ip_address):

    # Daca IP-ul este localhost sau un IP privat, folosim un IP public pentru test
    private_ip_prefixes = ('127.', '192.168.', '10.', '172.')
    if any(ip_address.startswith(prefix) for prefix in private_ip_prefixes):
        ip_address = get_public_ip()  # IP public al server-ului        

    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        response.raise_for_status()
        data = response.json()
        return data.get('street', ''), data.get('city', ''), data.get('region', ''), data.get('country', '')
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching location: {e}")
        



BANNED_EMAILS_FILE = os.path.join(os.getcwd(), 'banned_users', 'banned_emails.json')

def load_banned_emails():

    os.makedirs(os.path.dirname(BANNED_EMAILS_FILE), exist_ok=True)
    

    if os.path.exists(BANNED_EMAILS_FILE):
        with open(BANNED_EMAILS_FILE, 'r') as json_file:
            return json.load(json_file)
    return []  

def save_banned_emails(banned_emails):
    os.makedirs(os.path.dirname(BANNED_EMAILS_FILE), exist_ok=True)
    
    with open(BANNED_EMAILS_FILE, 'w') as json_file:
        json.dump(banned_emails, json_file)



def register_view(request):
    logger.info("--------------Functia register_view a fost apelata")
    banned_emails = load_banned_emails()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)


        if form.is_valid():
            email = form.cleaned_data.get('email')
                    
            if email in banned_emails:
                return render(request, "register.html", {"form": form, "error": f"Contul este interzis pentru tentativa de hacking!"})
            
            if form.cleaned_data.get('username').lower() == 'admin':
                if email not in banned_emails:
                    banned_emails.append(email)
                    save_banned_emails(banned_emails)
                    subject = 'Cineva incearca sa ne preia site-ul'
                    message_text = f"Un utilizator a incercat sa se inregistreze cu username-ul 'admin'. Email: {form.cleaned_data.get('email')}. IP: {request.META.get('REMOTE_ADDR')}"

                    data_to_save = {

                    "email": form.cleaned_data.get('email'),
                    "ip":    request.META.get('REMOTE_ADDR'),

                    }

                    folder_path = os.path.join(os.getcwd(), 'banned_users') # Path folder

                    os.makedirs(folder_path, exist_ok=True)

                    # Salvare data in json
                    current_date = datetime.now().strftime("%Y-%m-%d %M")
                    file_name = f"banned_{current_date}.json"
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'w') as json_file:
                        json.dump(data_to_save, json_file, indent=4)

                    message_html = f"""
                    <html>
                        <head>
                            <style>
                                h1 {{
                                    color: red;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1>{subject}</h1>
                            <p>{message_text}</p>
                        </body>
                    </html>
                    """

                    # Crearea mesajului multipart
                    email = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [admin_email for admin_email in settings.ADMINS])
                    email.attach_alternative(message_html, "text/html")
                    
                    # Trimiterea emailului
                    email.send()

                    return render(request, "register.html", {"form": form, "error": f"Username-ul '{form.cleaned_data.get('username')}' nu este disponibil."})

            user = form.save(commit=False)
            user.cod = ''.join(random.choices(string.ascii_letters + string.digits, k=20))  # Cod random
            user.email_confirmat = False 
            user.ip_address = request.META.get('REMOTE_ADDR')
            user.browser_info = request.META.get('HTTP_USER_AGENT', '')

            # Obtinere locatie user
            ip_address = request.META.get('REMOTE_ADDR')

            street, city, region, country = get_location(ip_address)

            user.location_street = street
            user.location_city = city
            user.location_region = region
            user.location_country = country

            user.save()

            subject = 'Confirmare Email'
            message = render_to_string('email/confirmation_email.html', {'user': user})
            send_mail(
                subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message = message
            )
            return redirect('cod_confirmare')
    else:
        form = CustomUserCreationForm()
    
    messages.debug(request, "Acesta este un mesaj de depanare!!!")
    logger.debug("--------------Functia register_view executata cu succes!")
    return render(request, "register.html", {"form": form})





def confirma_mail(request, cod):
    logger.info("--------------Functia confirma_email a fost apelata")
    try:
        user = CustomUser.objects.get(cod=cod)
        user.email_confirmat = True

        logger.info(f"Email confirmat pentru utilizator: {user.username}")

        user.save()

        logger.debug("--------------Functia confirma_mail executata cu succes!")
        return render(request, 'confirmation_success.html', {'message': 'Emailul a fost confirmat cu succes!'})
    except CustomUser.DoesNotExist:
       
        logger.warning(f"Codul de confirmare '{cod}' este invalida")
        send_error_email(f"Codul de confirmare '{cod}' este invalid.")
        return HttpResponseForbidden("Codul de confirmare este invalid.")
    
    except Exception as e:

        logger.critical(f"A aparut o eroare critica: {str(e)}")
        send_error_email(f"A aparut o eroare: {str(e)}")
        return HttpResponse("A aparut o eroare. Va rugăm sa incercati din nou mai tarziu.")

def send_error_email(error_message):
    logger.info("--------------Functia send_error_email a fost apelata")
    subject = 'Eroare la confirmarea emailului'
    message_text = f"A aparut o eroare: {error_message}"


    message_html = f"""
    <html>
        <head>
            <style>
                h1 {{
                    color: red;
                    background-color: #f8d7da;
                }}
            </style>
        </head>
        <body>
            <h1>{subject}</h1>
            <p>{message_text}</p>
        </body>
    </html>
    """


    email = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [admin_email for admin_email in settings.ADMINS])
    email.attach_alternative(message_html, "text/html")
    
    email.send()


failed_login_attempts = {}  

def custom_login_view(request):
    logger.info("--------------Functia custom_login_view a fost apelata")
    if request.method == 'POST':
        form = CustomAuthenticationForm(data = request.POST, request = request)
        username = form.data.get('username')
        ip_address = request.META.get('REMOTE_ADDR')
        

        if form.is_valid():
            user = authenticate(username = form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
            if user.is_blocked:
                messages.error(request, "Contul tau a fost blocat!!!!")
                return render(request, 'login.html')
            
            if user is None or not user.email_confirmat:
                record_failed_attempt(username, ip_address)

                if check_suspicious_activity(username):
                    print("Suspicious activity detected. Sending email...")
                    send_suspicious_login_email(username, ip_address)

                return render(request, 'login.html', {'form': form, 'error': 'Emailul nu este confirmat. Verificați emailul.'})
            
            login(request, user)
            return redirect('profile_view')
        else:
            record_failed_attempt(username, ip_address)
            if check_suspicious_activity(username):
                print("Suspicious activity detected. Sending email...")
                send_suspicious_login_email(username, ip_address)

    else:
        form = CustomAuthenticationForm()


    messages.debug(request, "Acesta este un mesaj de depanare!!!")
    logger.debug("--------------Functia custom_login_view executata cu succes!")
    return render(request, 'login.html', {'form': form})


def record_failed_attempt(username, ip_address):
    logger.info("--------------Functia record_failed_attemp a fost apelata")
    timestamp = timezone.now()
    if username not in failed_login_attempts:
        failed_login_attempts[username] = []
    failed_login_attempts[username].append((timestamp, ip_address))

def check_suspicious_activity(username):
    logger.info("--------------Functia check_suspicious_activity a fost apelata")
    if username in failed_login_attempts:
        attempts = failed_login_attempts[username]
        # Filtrare incercari care sunt mai vechi de 2 minute
        recent_attempts = [(ts, ip) for (ts, ip) in attempts if (timezone.now() - ts).total_seconds() < 120]
        return len(recent_attempts) >= 3
    return False

def send_suspicious_login_email(username, ip_address):
    logger.info("--------------Functia send_suspicious_login_email a fost apelata")
    subject = 'Logari suspecte'
    message_text = f"Un utilizator a incercat sa se logheze de 3 ori esuat folosind username-ul '{username}'. IP-ul: {ip_address}"

    message_html = f"""
    <html>
        <head>
            <style>
                h1 {{
                    color: red;
                }}
            </style>
        </head>
        <body>
            <h1>{subject}</h1>
            <p>{message_text}</p>
        </body>
    </html>
    """

    # Mesaj multipart
    email = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [admin_email for admin_email in settings.ADMINS])
    email.attach_alternative(message_html, "text/html")
    
    email.send()



@login_required
def profile_view(request):
    logger.info("--------------Functia profile_view a fost apelata")
    user = request.user

    messages.info(request, "Login executat cu succes :) ")
    messages.debug(request, "Acesta este un mesaj de depanare!!!")
    logger.debug("--------------Functia profile_view executata cu succes!")
    return render(request, 'profile.html', {'user': user})

@login_required
def change_password_view(request):
    logger.info("--------------Functia change_password_view a fost apelata")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            logger.debug("--------------Parola schimbata!")
            return redirect('profile_view')  # Dupa schimbarea parolei, redirectionează utilizatorul la profil
    else:
        form = PasswordChangeForm(request.user)

    logger.debug("--------------Functia change_password_view executata cu succes!")
    return render(request, 'change_password.html', {'form': form})


def logout_view(request):
    logger.info("--------------Functia logout_view a fost apelata")
    logout(request)
    
    logger.debug("--------------Functia logout_view executata cu succes!")
    return redirect('mesaj_trimis')



def adauga_vizualizare(utilizator, categorie):

    logger.info("--------------Functia adauga_vizualizare a fost apelata")

    if not Vizualizare.objects.filter(utilizator=utilizator, categorie=categorie).exists():
        Vizualizare.objects.create(utilizator=utilizator, categorie=categorie)

    vizualizari = Vizualizare.objects.filter(utilizator=utilizator).order_by('-data_vizualizare')
    if vizualizari.count() > 3:
        vizualizari.last().delete()





@login_required
def detalii_inghetata(request):
    logger.info("--------------Functia detalii_inghetata a fost apelata")
    inghetate = Inghetata.objects.all()  
    utilizator = request.user
    categorie = 'Inghetata'


    for inghetata in inghetate:
        adauga_vizualizare(utilizator, categorie)

    
    context = {
        'inghetate': inghetate,
        'categorie': categorie,
    }
    messages.warning(request, "Acesta este un avertisment. :| ")
    messages.error(request, "A aparut o eroare! >:((  ")
    logger.debug("--------------Functia detalii_inghetata executata cu succes!")
    return render(request, 'detalii_inghetata.html', context)


@login_required
def detalii_biscuit(request):
    logger.info("--------------Functia detalii_biscuit a fost apelata")
    biscuiti = Biscuite.objects.all()  
    utilizator = request.user
    categorie = 'Biscuiti'

   
    for biscuit in biscuiti:
        adauga_vizualizare(utilizator, categorie)

   
    context = {
        'biscuiti': biscuiti,
        'categorie': categorie,
    }
    logger.debug("--------------Functia detalii_biscuiti executata cu succes!")
    return render(request, 'detalii_biscuit.html', context)


@login_required
def detalii_bautura(request):
    logger.info("--------------Functia detalii_bautura a fost apelata")
    bauturi = Bauturi.objects.all()  
    utilizator = request.user
    categorie = 'Bauturi'


    for bautura in bauturi:
        adauga_vizualizare(utilizator, categorie)

 
    context = {
        'bauturi': bauturi,
        'categorie': categorie,
    }
    logger.debug("--------------Functia detalii_bautura executata cu succes!")
    return render(request, 'detalii_bautura.html', context)


@login_required
def detalii_prajitura(request):
    logger.info("--------------Functia detalii_prajitura a fost apelata")
    prajituri = Prajituri.objects.all()  
    utilizator = request.user
    categorie = 'Prajituri'

  
    for prajitura in prajituri:
        adauga_vizualizare(utilizator, categorie)


    context = {
        'prajituri': prajituri,
        'categorie': categorie,
    }
    logger.debug("--------------Functia detalii_prajitura executata cu succes!")
    return render(request, 'detalii_prajitura.html', context)


@login_required
def detalii_torturi(request):
    logger.info("--------------Functia detalii_torturi a fost apelata")
    torturi = Torturi_Inghetata.objects.all()  
    utilizator = request.user
    categorie = 'Torturi Inghetata'


    for tort in torturi:
        adauga_vizualizare(utilizator, categorie)


    context = {
        'torturi': torturi,
        'categorie': categorie,
    }
    logger.debug("--------------Functia detalii_torturi executata cu succes!")
    return render(request, 'detalii_tort_inghetata.html', context)





def is_admin(user):
    logger.info("--------------Functia is_admin a fost apelata")
    return user.is_staff  # Verifica daca utilizatorul este administrator

@user_passes_test(is_admin, login_url='https://www.youtube.com/watch?v=xvFZjo5PgG0')  # Redirectionare daca nu e admin
# @user_passes_test(is_admin, login_url='custom_login_view') 
@login_required
def creeaza_promotie(request):
    logger.info("--------------Functia creeaza_promotie a fost apelata")
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            promotie = form.save()

            # Apply discount to all products
            produse = Informatii.objects.all()  # Get all products
            for produs in produse:
                # Calculate new price after applying discount
                produs.pret = round(produs.pret * (1 - (promotie.discount / 100)), 2)
                produs.save()  # Save updated product price

            minim_vizualizari = form.cleaned_data['k']
            utilizatori_cu_vizualizari = Vizualizare.objects.values('utilizator').annotate(numar_vizualizari=Count('id')).filter(numar_vizualizari__gte=minim_vizualizari)

            utilizatori = CustomUser.objects.filter(id__in=[v['utilizator'] for v in utilizatori_cu_vizualizari])
            subject = f'Promotie Speciala: {promotie.nume}'
            from_email = "artchanell01@gmail.com"
            messages = []

            for utilizator in utilizatori:
                message = f"Salut {utilizator.username},\n\n"
                message += f"Avem o noua promotie pentru tine! Detaliile promotiei:\n"
                message += f"Nume: {promotie.nume}\n"
                message += f"Descriere: {promotie.descriere}\n"
                message += f"Discount: {promotie.discount}%\n"
                message += f"Data Expirarii: {promotie.data_expirare.strftime('%d-%m-%Y')}\n\n"
                message += "Nu rata aceasta oportunitate! Viziteaza-ne acum pentru mai multe detalii."
 
                messages.append((subject, message, from_email, [utilizator.email]))
              
            if messages:
                send_mass_mail(messages, fail_silently=False)

            logger.debug("--------------Promotie creata si preturi actualizate!")
            return redirect('mesaj_trimis') 

    else:
        form = PromotieForm()

    logger.debug("--------------Functia creaza_promotie executata cu succes!")
    return render(request, 'promotii.html', {'form': form})


def creste_preturi(request):
    if not request.user.is_superuser:
        mesaj_personalizat = "Accesul la informatiile despre meniu este restrictionat!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze meniul fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Acces Interzis',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)
    
    if request.method == 'POST':
        procent = Decimal(request.POST.get('procent', 0))  
        if procent > 0:
            produse = Informatii.objects.all()  
            for produs in produse:
               
                produs.pret = round(produs.pret * (1 + (procent / Decimal(100))), 2)
                produs.save() 
            
            messages.success(request, f"Preturile au fost crescute cu {procent}%!")
            return redirect('mesaj_trimis')

    return render(request, 'creste_preturi.html')






def afisare_pagina(request):
    logger.debug("--------------Functia afisare_pagina a fost apelata")

    try:
        result = 10 / 0  # Simulare operatiune care va genera eroare de tip ZeroDivisionError
    except ZeroDivisionError as e:
        logger.error("Eroare la calcul: %s", str(e))
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return HttpResponse("A aparut o eroare în procesare")

    logger.info("--------------Functia afisare_pagina a fost executata cu succes!")
    return HttpResponse("Pagina a fost afisata cu succes!")



def adauga_prajitura(request):
    logger.info("--------------Functia adauga_prajitura a fost apelata")


    if not request.user.has_perm('gelaterie.add_prajituri') :
        mesaj_personalizat = "Nu ai voie sa adaugi prajituri!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze formularul de adaugare prajituri fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Eroare adaugare produse',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    if request.method == 'POST':
        form = PrajituriForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Prajitura a fost adaugată cu succes!")
            return redirect('mesaj_trimis') 
    else:
        form = PrajituriForm()

    logger.info("--------------Functia adauga_prajitura a fost executata cu succes!")
    return render(request, 'adauga_prajitura.html', {'form': form})



def oferta(request):

    if not request.user.has_perm('vizualizeaza_oferta'):
        mesaj_personalizat = "Nu ai voie sa vizualizezi oferta!"
        logger.warning(f"Utilizatorul {request.user.username if request.user.is_authenticated else 'anonim'} a incercat sa acceseze oferta fara permisiune!")
        messages.warning(request, "Acesta este un avertisment. :| ")
        messages.error(request, "A aparut o eroare! >:((  ")
        return render(request, '403.html', {
            'title': 'Eroare afisare oferta',
            'mesaj_personalizat': mesaj_personalizat,
            'user': request.user,
        }, status=403)

    messages.info(request, "Oferta accesata cu succes :) ")
    logger.info("--------------Functia oferta a fost executata cu succes!")
    return render(request, 'oferta.html', {'message': 'Reducere 50%! Profitati acum!'})


@login_required
def accepta_oferta(request):
    if request.method == 'POST':
        request.user.user_permissions.add(Permission.objects.get(codename='vizualizeaza_oferta'))
        return JsonResponse({'success': True})
    

    logger.info("--------------Functia accepta_oferta a fost executata cu succes!")
    return JsonResponse({'success': False}, status=400)





moderators_group, created = Group.objects.get_or_create(name="Moderatori") # Grup Moderatori creare

# Permisiuni la grupul Moderatori
content_type = ContentType.objects.get_for_model(CustomUser)

permissions = [
    "view_customuser",  
    "change_customuser"  
]

for codename in permissions:
    permission = Permission.objects.get(codename = codename, content_type = content_type) # Cautare in baza de date a permisiunilor 
    moderators_group.permissions.add(permission)





def genereaza_factura_pdf(user, comanda, total_price, comanda_data):
    folder_path = os.path.join('temporar-facturi', user.username)
    os.makedirs(folder_path, exist_ok=True)
    timestamp = int(time.time())
    file_name = f"factura-{timestamp}.pdf"
    file_path = os.path.join(folder_path, file_name)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Titlu
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Factură - Gelaterie")

    # Date client
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(50, y, f"Nume: {user.first_name} {user.last_name}")
    c.drawString(50, y - 20, f"Email: {user.email}")
    c.drawString(50, y - 40, f"Data comenzii: {comanda.data_achizitie}")

    y -= 80
    c.drawString(50, y, "Produse comandate:")
    y -= 20

    # Produse
    for item in comanda_data:
        informatii = Informatii.objects.get(id=item['id'])
        line = f"{informatii.specificatii} - Cantitate: {item['cantitate']} - Pret unitar: {informatii.pret} RON"
        c.drawString(50, y, line)
        y -= 20

    # Totaluri
    y -= 40
    c.drawString(50, y, f"Total obiecte: {sum(item['cantitate'] for item in comanda_data)}")
    c.drawString(50, y - 20, f"Pret total: {total_price} RON")

    c.save()
    return file_path



def send_invoice_email(user, pdf_path):
    subject = "Factura ta - Gelaterie"
    body = (
        f"Salut {user.first_name},\n\n"
        "Aici ai factura pentru comanda ta.\n\n"
        "Multumim că ai ales Gelateria noastra!\n"
        "Cu drag, echipa Pufic:)"
    )
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_file(pdf_path)
    email.send()


