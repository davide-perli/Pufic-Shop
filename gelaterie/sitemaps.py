from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import (
    Sponsor, Magazine, Adresa, Alergeni, Informatii, 
    Inghetata, Biscuite, Bauturi, Prajituri, Torturi_Inghetata
)

class SponsorSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Sponsor.objects.all()

    def location(self, obj):
        return reverse('sponsori')  

class MagazineSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8

    def items(self):
        return Magazine.objects.all()

    def location(self, obj):
        return reverse('magazine')  

class AdresaSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Adresa.objects.all()

    def location(self, obj):
        return reverse('adresa')  

class AlergeniSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return Alergeni.objects.all()

    def location(self, obj):
        return reverse('afiseaza_alergeni')  

class InformatiiSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Informatii.objects.all()

    def location(self, obj):
        return reverse('informatii')  

class InghetataSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Inghetata.objects.all()

    def location(self, obj):
        return reverse('inghetata')  

class BiscuiteSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Biscuite.objects.all()

    def location(self, obj):
        return reverse('biscuiti')  

class BauturiSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Bauturi.objects.all()

    def location(self, obj):
        return reverse('bauturi')  

class PrajituriSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.85

    def items(self):
        return Prajituri.objects.all()

    def location(self, obj):
        return reverse('prajituri')  

class TorturiInghetataSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.85

    def items(self):
        return Torturi_Inghetata.objects.all()

    def location(self, obj):
        return reverse('torturi_inghetata')  
