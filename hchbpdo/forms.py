from django import forms


class PdoForm(forms.Form):
    balance = forms.FloatField(label="Current balance (in hours)")
    days = forms.FloatField(label="Scheduled PDO days")
    target_date = forms.DateField(label="Target Date")