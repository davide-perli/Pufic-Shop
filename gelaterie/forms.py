from django import forms
from datetime import date
import re
from .models import Comanda
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from .models import Promotie


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
    # Returnez direct email-ul validat
        return self.cleaned_data.get("email", "").strip()
    def clean_confirm_email(self):
    # Returnez direct confirm_email-ul validat
        return self.cleaned_data.get("confirm_email", "").strip()

    def clean(self):
        # Preluare date curatate
        cleaned_data = super().clean()

        # Validare email-uri proprie (nu merge cu ce e in curs)
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if not email or not confirm_email: # Nu campuri goale
            raise forms.ValidationError("Ambele câmpuri de email trebuie completate.")

        if confirm_email == email:
            return cleaned_data
        self.add_error("confirm_email", "Adresele de email nu coincid.") # Imi trebuie una specifica, altfel nu se afiseaza

        


    def clean_zile(self):
        zile_asteptare = self.cleaned_data.get('zile_asteptare')
        if  zile_asteptare < 0:  # Validare zile de asteptare
            raise forms.ValidationError("Numarul minim de zile de asteptare trebuie sa fie mai mare ca 0")
        return zile_asteptare

    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        if data_nasterii:
            today = date.today()
            age = today.year - data_nasterii.year
            
            if age < 18: # Doar utilizatori majori
                raise forms.ValidationError("Trebuie sa fii major (18+) pentru a completa acest formular.")
        return data_nasterii
    
    def clean_mesaj(self):
        mesaj = self.cleaned_data.get('mesaj').strip()
        nume_utilizator = self.cleaned_data.get('nume').strip()  # Preluare nume pentru semnatura

        cuvinte = re.findall(r'\b\w+\b', mesaj)  # Cuvinte alfanumerice
        if len(cuvinte) < 5 or len(cuvinte) > 100:
            raise forms.ValidationError("Mesajul trebuie sa contina intre 5 si 100 de cuvinte.")

        if re.search(r'\bhttps?://\S+', mesaj):  # Link detect
            raise forms.ValidationError("Mesajul nu poate contine linkuri.")

        if not mesaj.lower().endswith(nume_utilizator.lower()): #verificare semnatura   
            raise forms.ValidationError(f"Mesajul trebuie sa se termine cu numele utilizatorului: {nume_utilizator}")

        return mesaj
    
    def clean_validare_comuna(self, value, field_name):
        if not value:
            return value #Asa pot avea camp gol pentru prenume
        
        if not value[0].isupper():
                    raise forms.ValidationError(f"{field_name} trebuie sa inceapa cu litera mare.")

        if not all(char.isalpha() or char.isspace() for char in value):
                    raise forms.ValidationError(f"{field_name} poate contine doar litere si spatii.")
        


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
        help_text = "Adaugati o notita pentru comanda"
    )
    discount_procent = forms.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        required = False,
        label = "Discount (%)",
        help_text = "Introduceti procentul de discount (0-100)"
    )


    class Meta:
        model = Comanda
        fields = ['livrare_curier', 'informatii'] # Preluare coloane dintre cele existente
        labels = {
            'livrare_curier': "Livrare curier",
            'informatii': "Informatii comandă",
        }
        widgets = {
            'informatii': forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}), # Pentru a selecta mai multe comenzi
        }

    def clean_cos_cumparaturi(self):
        cos_cumparaturi = self.cleaned_data.get('cos_cumparaturi')
        if not cos_cumparaturi[0].isupper():
            raise forms.ValidationError("Cosul de cumparaturi trebuie sa inceapa cu o litera mare")
        return cos_cumparaturi

    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note and not note[0].isupper():
            raise forms.ValidationError("Notele trebuie să înceapă cu literă mare.")
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
                    "Cosul de cumparaturi trebuie să includa minim una dintre specificatiile produselor selectate."
                )

        return cleaned_data
    


class CustomUserCreationForm(UserCreationForm):
    telefon = forms.CharField(
        max_length=15,
        required=False,
        label="Telefon",
        help_text="Introduceti un numar de telefon valid",
    )
    adresa = forms.CharField(
        max_length=150,
        required=False,
        label="Adresa",
        help_text="Introduceti adresa completa",
    )
    age = forms.IntegerField(
        required=True,
        label="Varsta",
        help_text="Trebuie sa fi  major",
    )
    sex = forms.ChoiceField(
        choices=CustomUser.optiuni_sex,
        required=True,
        label="Sex",
    )
    nationalitate = forms.CharField(
        max_length=50,
        required=True,
        label="Nationalitate",
        help_text="Introduceti nationalitatea dvs.",
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "telefon",
            "adresa",
            "age",
            "sex",
            "nationalitate",
        ]

    def clean_telefon(self):
        telefon = self.cleaned_data.get("telefon")
        if telefon and not telefon.isdigit():
            raise forms.ValidationError("Numarul de telefon trebuie sa contina doar cifre!")
        return telefon

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("Trebuie sa fii major!")
        return age

    def clean_nationalitate(self):
        nationalitate = self.cleaned_data.get("nationalitate")
        if not nationalitate.isalpha():
            raise forms.ValidationError("Nationalitatea trebuie sa contina doar litere!")
        return nationalitate
    


class CustomAuthenticationForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat'
    )

    def clean(self):        
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data
    



from django import forms
from .models import Promotie

class PromotieForm(forms.ModelForm):
    k = forms.IntegerField(required=True, label="Minim Vizualizari", min_value=1)
    data_expirare = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data Expirării"
    )

    class Meta:
        model = Promotie
        fields = ['nume', 'data_expirare', 'categorie', 'descriere', 'discount', 'k']

