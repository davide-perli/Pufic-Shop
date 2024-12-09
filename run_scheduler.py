import os
import django
import schedule
import time
import sys

# Setează corect DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proiect.settings')  # Asigură-te că este corect
django.setup()

# Importuri după configurare
from gelaterie.tasks import delete_unconfirmed_users, send_newsletter, send_hello, send_daily_report

def run_scheduler():
    schedule.every(1).minutes.do(delete_unconfirmed_users)
    #schedule.every().day.at("15:11").do(send_newsletter)
    schedule.every(1).minutes.do(send_hello)
    schedule.every().day.at("15:11").do(send_daily_report)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("Scheduler oprit manual.")
        sys.exit()
