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
import decimal
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

import random
import string


from django.core.mail import send_mass_mail
from .models import  Vizualizare
from django.utils.timezone import now
from .forms import PromotieForm
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test

from django.core.mail import EmailMultiAlternatives


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


@login_required(login_url='custom_login_view')  # Redirectioneaza la login daca nu e autentificat
def adauga_comanda(request):
    inghetata_items = Inghetata.objects.all()
    bauturi_items = Bauturi.objects.all()
    biscuiti_items = Biscuite.objects.all()
    prajituri_items = Prajituri.objects.all()
    torturi_items = Torturi_Inghetata.objects.all()

    if request.method == 'POST':
        form = ComandaForm(request.POST)
        if form.is_valid():
            comanda = form.save(commit=False)
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

            comanda.note = note
            comanda.cos_cumparaturi = cos_cumparaturi
            comanda.save()
            form.save_m2m()

            return redirect('mesaj_trimis')
    else:
        form = ComandaForm()

    context = {
        'form': form,
        'inghetata_items': inghetata_items,
        'bauturi_items': bauturi_items,
        'biscuiti_items': biscuiti_items,
        'prajituri_items': prajituri_items,
        'torturi_items': torturi_items,
    }

    return render(request, 'adauga_comanda.html', context)




def get_site_url(request=None):
    if request:
        # Daca exista un request, determin automat host-ul
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        return f"{scheme}://{host}"
    # Implicit varianta pentru IP
    return "http://192.168.0.103:8000"



def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            
            if form.cleaned_data.get('username').lower() == 'admin':
                subject = 'Cineva incearca sa ne preia site-ul'
                message_text = f"Un utilizator a incercat sa se inregistreze cu username-ul 'admin'. Email: {form.cleaned_data.get('email')}"

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
            user.save()

            subject = 'Confirmare Email'
            message = render_to_string('email/confirmation_email.html', {'user': user})
            send_mail(
                subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message
            )
            return redirect('custom_login_view')
    else:
        form = CustomUserCreationForm()
    
    return render(request, "register.html", {"form": form})



from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from .models import CustomUser
from django.conf import settings

def confirma_mail(request, cod):
    try:
        user = CustomUser.objects.get(cod=cod)
        user.email_confirmat = True
        user.save()
        return render(request, 'confirmation_success.html', {'message': 'Emailul a fost confirmat cu succes!'})
    except CustomUser.DoesNotExist:
       
        send_error_email(f"Codul de confirmare '{cod}' este invalid.")
        return HttpResponseForbidden("Codul de confirmare este invalid.")
    
    except Exception as e:

        send_error_email(f"A aparut o eroare: {str(e)}")
        return HttpResponse("A aparut o eroare. Va rugăm sa incercati din nou mai tarziu.")

def send_error_email(error_message):
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
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        username = form.data.get('username')
        ip_address = request.META.get('REMOTE_ADDR')
        

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
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
    
    return render(request, 'login.html', {'form': form})


def record_failed_attempt(username, ip_address):
    timestamp = timezone.now()
    if username not in failed_login_attempts:
        failed_login_attempts[username] = []
    failed_login_attempts[username].append((timestamp, ip_address))

def check_suspicious_activity(username):
    if username in failed_login_attempts:
        attempts = failed_login_attempts[username]
        # Filtrare incercari care sunt mai vechi de 2 minute
        recent_attempts = [(ts, ip) for (ts, ip) in attempts if (timezone.now() - ts).total_seconds() < 120]
        return len(recent_attempts) >= 3
    return False

def send_suspicious_login_email(username, ip_address):
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
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Dupa schimbarea parolei, redirectionează utilizatorul la profil
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('mesaj_trimis')





def adauga_vizualizare(utilizator, categorie):

    if not Vizualizare.objects.filter(utilizator=utilizator, categorie=categorie).exists():
        Vizualizare.objects.create(utilizator=utilizator, categorie=categorie)

    vizualizari = Vizualizare.objects.filter(utilizator=utilizator).order_by('-data_vizualizare')
    if vizualizari.count() > 3:
        vizualizari.last().delete()





@login_required
def detalii_inghetata(request):
    inghetate = Inghetata.objects.all()  
    utilizator = request.user
    categorie = 'Inghetata'


    for inghetata in inghetate:
        adauga_vizualizare(utilizator, categorie)

    
    context = {
        'inghetate': inghetate,
        'categorie': categorie,
    }

    return render(request, 'detalii_inghetata.html', context)


@login_required
def detalii_biscuit(request):
    biscuiti = Biscuite.objects.all()  
    utilizator = request.user
    categorie = 'Biscuiti'

   
    for biscuit in biscuiti:
        adauga_vizualizare(utilizator, categorie)

   
    context = {
        'biscuiti': biscuiti,
        'categorie': categorie,
    }

    return render(request, 'detalii_biscuit.html', context)


@login_required
def detalii_bautura(request):
    bauturi = Bauturi.objects.all()  
    utilizator = request.user
    categorie = 'Bauturi'


    for bautura in bauturi:
        adauga_vizualizare(utilizator, categorie)

 
    context = {
        'bauturi': bauturi,
        'categorie': categorie,
    }

    return render(request, 'detalii_bautura.html', context)


@login_required
def detalii_prajitura(request):
    prajituri = Prajituri.objects.all()  
    utilizator = request.user
    categorie = 'Prajituri'

  
    for prajitura in prajituri:
        adauga_vizualizare(utilizator, categorie)


    context = {
        'prajituri': prajituri,
        'categorie': categorie,
    }

    return render(request, 'detalii_prajitura.html', context)


@login_required
def detalii_torturi(request):
    torturi = Torturi_Inghetata.objects.all()  
    utilizator = request.user
    categorie = 'Torturi Inghetata'


    for tort in torturi:
        adauga_vizualizare(utilizator, categorie)


    context = {
        'torturi': torturi,
        'categorie': categorie,
    }

    return render(request, 'detalii_tort_inghetata.html', context)





def is_admin(user):
    return user.is_staff  # Verifica daca utilizatorul este administrator

@user_passes_test(is_admin, login_url='https://www.youtube.com/watch?v=xvFZjo5PgG0')  # Redirectionare daca nu e admin
# @user_passes_test(is_admin, login_url='custom_login_view') 
@login_required
def creeaza_promotie(request):
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
           
            promotie = form.save()

            minim_vizualizari = form.cleaned_data['k']

            # Nr utilizatori cu nr minim de vizualizari
            utilizatori_cu_vizualizari = Vizualizare.objects.values('utilizator').annotate(numar_vizualizari=Count('id')).filter(numar_vizualizari__gte=minim_vizualizari)

            # Obtinere utilizatori
            utilizatori = CustomUser.objects.filter(id__in=[v['utilizator'] for v in utilizatori_cu_vizualizari])

            subject = f'Promotie Speciala: {promotie.nume}'

            for utilizator in utilizatori:
        
                message = f"Salut {utilizator.username},\n\n"
                message += f"Avem o noua promotie pentru tine! Detaliile promotiei:\n"
                message += f"Nume: {promotie.nume}\n"
                message += f"Descriere: {promotie.descriere}\n"
                message += f"Discount: {promotie.discount}%\n"
                message += f"Data Expirarii: {promotie.data_expirare.strftime('%d-%m-%Y')}\n"
                message += f"Categorie: {promotie.categorie}\n\n"
                message += "Nu rata aceasta oportunitate! Viziteaza-ne acum pentru mai multe detalii."

              
                send_mail(
                    subject, 
                    message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [utilizator.email]
                )

            return redirect('mesaj_trimis') 

    else:
        form = PromotieForm()

    return render(request, 'promotii.html', {'form': form})

