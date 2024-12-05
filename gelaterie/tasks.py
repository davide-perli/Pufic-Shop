import django
import os
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser  


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proiect.settings')
django.setup()

def delete_unconfirmed_users():

    threshold = timezone.now() - timezone.timedelta(minutes = 2)  # Utilizatorii neconfirmati mai vechi de 2 de minute
    unconfirmed_users = CustomUser.objects.filter(email_confirmat = False, date_joined__lt = threshold)
    count = unconfirmed_users.count()
    unconfirmed_users.delete()
    print(f"{count} utilizatori neconfirmati au fost stersi!")

def send_newsletter():
 
    threshold = timezone.now() - timezone.timedelta(minutes = 1440)  # 1 zi
    users = CustomUser.objects.filter(email_confirmat = True, date_joined__lt = threshold)
    for user in users:
        subject = "Newsletter zilnic"
        message = "Acesta este newsletterul dvs. zilnic!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    print(f"Newsletter trimis la {users.count()} utilizatori!")

def send_hello():
    
    print("Salut! Ce mai faci?")

def send_daily_report():

    print("Raportul zilnic a fost trimis!")