from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    SponsorSitemap, MagazineSitemap, AdresaSitemap, AlergeniSitemap, InformatiiSitemap,
    InghetataSitemap, BiscuiteSitemap, BauturiSitemap, PrajituriSitemap, TorturiInghetataSitemap
)

# python manage.py runserver 0.0.0.0:8000
# http://192.168.0.103:8000


sitemaps = {
    'sponsor': SponsorSitemap,
    'magazine': MagazineSitemap,
    'adresa': AdresaSitemap,
    'alergeni': AlergeniSitemap,
    'informatii': InformatiiSitemap,
    'inghetata': InghetataSitemap,
    'biscuiti': BiscuiteSitemap,
    'bauturi': BauturiSitemap,
    'prajituri': PrajituriSitemap,
    'torturi_inghetata': TorturiInghetataSitemap,
}



urlpatterns = [
    path('', views.display_items, name = 'display_items'),
    path("home", views.home, name = "home"),
    path("adresa", views.adresa, name = "adresa"),
    path("alergeni", views.afiseaza_alergeni, name = "afiseaza_alergeni"),
    path("bauturi", views.bauturi, name = "bauturi"),
    path("inghetata", views.inghetata, name = "inghetata"),
    path("biscuiti", views.biscuiti, name = "biscuiti"),
    path("prajituri", views.prajituri, name = "prajituri"),
    path("torturi-inghetata", views.torturi_inghetata, name = "torturi_inghetata"),
    path("meniu", views.meniu, name = "meniu"),
    path("comenzi", views.comenzi, name = "comenzi"),
    path("sponsori", views.sponsori, name = "sponsori"),
    path("magazine", views.magazine, name = "magazine"),
    path("informatii", views.informatii, name = "informatii"),
    path('produse', views.display_products, name = "display_products"),
    path('contact', views.contact_view, name = "contact_view"),
    path('mesaj_trimis', views.mesaj_trimis, name = "mesaj_trimis"),
    path('cod_confirmare', views.cod_confirmare, name = "cod_confirmare"),
    path('adaugare', views.adauga_comanda, name = "adauga_comanda"),
    path('login', views.custom_login_view, name = "custom_login_view"),
    path('register', views.register_view, name = "register_view"),
    path('logout', views.logout_view, name = "logout_view"),
    path('profile', views.profile_view, name = "profile_view"),
    path('schimbare_parola', views.change_password_view, name = "change_password_view"),
    path('confirma_mail/<str:cod>', views.confirma_mail, name = "confirma_mail"),  # Ruta pentru confirmarea emailului
    path('promotii', views.creeaza_promotie, name = "promotii"), 
    path('detalii_inghetata', views.detalii_inghetata, name = "detalii_inghetata"),
    path('detalii_bautura', views.detalii_bautura, name = "detalii_bautura"),
    path('detalii_biscuit', views.detalii_biscuit, name = "detalii_biscuit"),
    path('detalii_prajitura', views.detalii_prajitura, name = "detalii_prajitura"),
    path('detalii_tort_inghetata', views.detalii_torturi, name = "detalii_tort_inghetata"),
    path('debug', views.afisare_pagina, name = "afisare_pagina"),
    path('adauga_prajitura', views.adauga_prajitura, name = "adauga_prajitura"),
    path('oferta', views.oferta, name = "oferta"),
    path('accepta-oferta', views.accepta_oferta, name = "accepta_oferta"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name = 'sitemap'),
    path('comanda_salvare', views.comanda_salvare, name = "comanda_salvare"),
    path('creste_preturi', views.creste_preturi, name = "creste_preturi")

]





# Forbidden (403)
# CSRF verification failed. Request aborted.

# Help
# Reason given for failure:

#     CSRF token from POST incorrect.
    
# In general, this can occur when there is a genuine Cross Site Request Forgery, or when Django’s CSRF mechanism has not been used correctly. For POST forms, you need to ensure:

# Your browser is accepting cookies.
# The view function passes a request to the template’s render method.
# In the template, there is a {% csrf_token %} template tag inside each POST form that targets an internal URL.
# If you are not using CsrfViewMiddleware, then you must use csrf_protect on any views that use the csrf_token template tag, as well as those that accept the POST data.
# The form has a valid CSRF token. After logging in in another browser tab or hitting the back button after a login, you may need to reload the page with the form, because the token is rotated after a login.
# You’re seeing the help section of this page because you have DEBUG = True in your Django settings file. Change that to False, and only the initial error message will be displayed.

# You can customize this page using the CSRF_FAILURE_VIEW setting.