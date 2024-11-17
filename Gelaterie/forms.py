from django import forms
from datetime import date
import re

class PrajituriFilterForm(forms.Form):
    nume = forms.CharField(required = False, label = 'Nume prăjitură')
    pret_min = forms.DecimalField(required = False, label = 'Preț minim', decimal_places = 2)
    pret_max = forms.DecimalField(required = False, label = 'Preț maxim', decimal_places = 2)
    alergeni_in = forms.CharField(required = False, label = 'Alergeni')
    magazin_disponibil = forms.DecimalField(required = False, label = 'Magazin disponibil')

class ContactForm(forms.Form):
    nume = forms.CharField(max_length = 10, label = 'Nume', required = True)
    prenume = forms.CharField(label = 'Prenume', required = False)
    data_nasterii = forms.DateField(label = 'Data nasterii', required = True)
    email = forms.EmailField(label = 'Email', required = True)
    confirm_email = forms.EmailField(label='Confirmare Email', required = True)
    optiuni_mesaj = (
        ("RECLAMATIE", "reclamatie"),
        ("INTREBARE", "intrebare"),
        ("REVIEW", "review"),
        ("CERERE", "cerere"),
        ("PROGRAMARE", "programare"),
    )
    tip_mesaj = forms.ChoiceField(choices = optiuni_mesaj, label = 'Tip mesaj')
    subiect = forms.CharField(label = 'Subiect', required = True)
    zile_asteptare = forms.IntegerField(label = 'Minim zile asteptare')
    mesaj = forms.CharField(max_length = 100 ,label = 'Mesaj')

    def clean_email(self):
    # Returnăm direct email-ul validat
        return self.cleaned_data.get("email", "").strip()

    def clean(self):
        # Preluăm toate datele curățate
        cleaned_data = super().clean()

        # Validăm email-urile
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if not email or not confirm_email: # Nu campuri goale
            raise forms.ValidationError("Ambele câmpuri de email trebuie completate.")

        if confirm_email == email:
            return cleaned_data
        self.add_error("confirm_email", "Adresele de email nu coincid.") # Imi trebuie o una specifica, altfel nu se afiseaza

        


    def clean_zile(self):
        zile_asteptare = self.cleaned_data.get('zile_asteptare')
        if  zile_asteptare < 0:
            raise forms.ValidationError("Numarul minim de zile de asteptare trebuie sa fie mai mare ca 0")
        return zile_asteptare

    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        if data_nasterii:
            today = date.today()
            age = today.year - data_nasterii.year
            
            if age < 18:
                raise forms.ValidationError("Trebuie sa fii major (18+) pentru a completa acest formular.")
        return data_nasterii
    
    def clean_mesaj(self):
        mesaj = self.cleaned_data.get('mesaj')
        nume_utilizator = self.cleaned_data.get('nume')  # Preluare nume pentru semnatura

        cuvinte = re.findall(r'\b\w+\b', mesaj)  # Cuvinte alfanumerice
        if len(cuvinte) < 5 or len(cuvinte) > 100:
            raise forms.ValidationError("Mesajul trebuie să conțină între 5 și 100 de cuvinte.")

        if re.search(r'\bhttps?://\S+', mesaj):  # Link detect
            raise forms.ValidationError("Mesajul nu poate conține linkuri.")

        if not mesaj.strip().endswith(nume_utilizator): #verificare semnatura
            raise forms.ValidationError(f"Mesajul trebuie să se termine cu numele utilizatorului: {nume_utilizator}")

        return mesaj
    
    def clean_validare_comuna(self, value, field_name):
        if not value:
            return value #Asa pot avea camp gol pentru prenume
        
        if not value[0].isupper():
                    raise forms.ValidationError(f"{field_name} trebuie să înceapă cu literă mare.")

        if not all(char.isalpha() or char.isspace() for char in value):
                    raise forms.ValidationError(f"{field_name} poate conține doar litere și spații.")
        

from django import forms
from .models import Comanda, Informatii

class ComandaForm(forms.ModelForm):
    # Campuri aditionale
    cos_cumparaturi = forms.CharField(
         max_length = 300,
         required = True,
         label = "Cos cumparaturi",
         help_text = "Adaugati produsele  pe care le doriti"
    )
    note = forms.CharField(
        max_length = 150,
        required = False,
        label = "Note",
        help_text = "Adăugați o notiță pentru comandă."
    )
    discount_procent = forms.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        required = False,
        label = "Discount (%)",
        help_text = "Introduceți procentul de discount (0-100)."
    )

    class Meta:
        model = Comanda
        fields = ['livrare_curier', 'informatii']
        labels = {
            'livrare_curier': "Livrare curier",
            'informatii': "Informații comandă",
        }
        widgets = {
            'informatii': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean_cos_cumparaturi(self):
        cos_cumparaturi = self.cleaned_data.get('cos_cumparaturi')
        if not cos_cumparaturi[0].isupper():
            raise forms.ValidationError("Cosul de cumparaturi trebuie sa inceapa cu o litera mare")
        return cos_cumparaturi

    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note is not None and not note[0].isupper():
            raise forms.ValidationError("Notita trebuie sa inceapa cu o litera mare.")
        return note

    def clean_discount_procent(self):
        discount = self.cleaned_data.get('discount_procent')
        if discount is not None and (discount < 0 or discount > 100):
            raise forms.ValidationError("Discount-ul trebuie sa fie intre 0 și 100%.")
        return discount
    
    def clean(self):
        cleaned_data = super().clean()
        cos_cumparaturi = cleaned_data.get('cos_cummparaturi')
        informatii = cleaned_data.get('informatii')

        if informatii and cos_cumparaturi:

            specificatii_list = [info.specificatii for info in informatii]
            if not any(spec in cos_cumparaturi for spec in specificatii_list):
                raise forms.ValidationError(
                    "Cosul de cumparaturi trebuie să includa una dintre specificatiile produselor selectate."
                )

        return cleaned_data

