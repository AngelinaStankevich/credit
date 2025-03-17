from django import forms
from .models import CreditApplication


class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        fields = ['amount', 'duration']
