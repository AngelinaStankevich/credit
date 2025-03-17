from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Client, CreditApplication
from .forms import CreditApplicationForm


def home(request):
    return render(request, 'credits/home.html')


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, 'credits/dashboard.html')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)  # Создаём профиль клиента при регистрации
            login(request, user)  # Автоматически логиним пользователя после регистрации
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def submit_credit_application(request):
    client, created = Client.objects.get_or_create(user=request.user)  # Создаём профиль, если его нет

    if request.method == "POST":
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = client
            application.save()
            return redirect('credit_applications_list')
    else:
        form = CreditApplicationForm()

    return render(request, 'credits/submit_credit.html', {'form': form})


@login_required
def credit_applications_list(request):
    client, created = Client.objects.get_or_create(user=request.user)
    applications = CreditApplication.objects.filter(client=client)
    return render(request, 'credits/credit_applications_list.html', {'applications': applications})
