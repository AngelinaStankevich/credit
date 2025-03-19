from django import forms
from .models import CreditApplication
from django.contrib.auth.forms import UserCreationForm
from .models import User, Client


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


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Роль")

    class Meta:
        model = User
        fields = ('username', 'role', 'password1', 'password2')


class PassportUploadForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["passport_scan"]  # Поле, куда загружается файл


class CreditDecisionForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        fields = ["status"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['avatar']