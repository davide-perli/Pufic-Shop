from django.urls import path
from . import views

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
    path('adaugare', views.adauga_comanda, name = "adauga_comanda"),
    path('login', views.custom_login_view, name = "custom_login_view"),
    path('register', views.register_view, name = "register_view"),
    path('logout', views.logout_view, name = "logout_view"),
    path('profile', views.profile_view, name = 'profile_view'),
    path('schimbare_parola', views.change_password_view, name = "change_password_view")
]