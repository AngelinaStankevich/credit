from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import CreditApplicationForm
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'credits/home.html')


@login_required(login_url='/accounts/login/')  # Перенаправление на страницу входа
def dashboard(request):
    if not hasattr(request.user, 'client'):
        Client.objects.create(user=request.user)  # Автоматическое создание профиля

    return render(request, 'credits/dashboard.html')  # Убедись, что этот шаблон существует


@login_required
def apply_credit(request):
    if request.method == 'POST':
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = request.user.client
            application.save()
            return redirect('dashboard')
    else:
        form = CreditApplicationForm()
    return render(request, 'credits/apply_credit.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # После регистрации перенаправляем на вход
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})