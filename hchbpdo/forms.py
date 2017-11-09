from django import forms


class PdoForm(forms.Form):
    balance = forms.FloatField(label="Current balance")
    days = forms.FloatField(label="Scheduled PDO days")