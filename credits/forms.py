from django import forms
from .models import CreditApplication


class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        fields = ['amount', 'duration']
        labels = {
            'amount': 'Сумма кредита',
            'duration': 'Срок кредита (в месяцах)',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
