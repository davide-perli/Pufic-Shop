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
    confirm_email = forms.EmailField(label='Confirmare Email')
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
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Adresele de email nu coincid.")
        
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