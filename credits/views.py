from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Client, CreditApplication
from .forms import CreditApplicationForm, PassportUploadForm, CreditDecisionForm, CustomUserCreationForm

def home(request):
    """Главная страница"""
    return render(request, 'credits/home.html')


@login_required
def dashboard(request):
    """Личный кабинет, показывает разные страницы для клиентов и сотрудников банка"""
    if request.user.role == 'bank_employee':
        return redirect('manage_applications')  # Страница для сотрудников банка
    return render(request, 'credits/dashboard.html')  # Страница для клиентов


def signup(request):
    """Регистрация пользователей с созданием профиля клиента"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            if user.role == 'client':  # Если роль клиента, создаём профиль
                Client.objects.create(user=user)
            login(request, user)  # Авторизуем пользователя
            if user.role == 'client':
                return redirect("dashboard")  # Для клиента перенаправляем в личный кабинет
            elif user.role == 'bank_employee':
                return redirect("manage_applications")  # Для сотрудника банка на страницу управления заявками
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def submit_credit_application(request):
    """Подача заявки на кредит (только для клиентов)"""
    if request.user.role != 'client':
        return redirect('dashboard')  # Если не клиент, перенаправляем на личную страницу

    client, created = Client.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = client
            application.status = 'pending'  # Статус заявки на рассмотрении
            application.save()
            return redirect('credit_applications_list')  # Перенаправление на список заявок
    else:
        form = CreditApplicationForm()

    return render(request, 'credits/submit_credit.html', {'form': form})


@login_required
def credit_applications_list(request):
    """Просмотр списка заявок (для клиентов и сотрудников)"""
    if request.user.role == 'client':
        client, _ = Client.objects.get_or_create(user=request.user)
        applications = CreditApplication.objects.filter(client=client)
    else:
        applications = CreditApplication.objects.all()  # Все заявки для сотрудников банка

    return render(request, 'credits/credit_applications_list.html', {'applications': applications})


@login_required
def manage_applications(request):
    """Управление заявками (только для сотрудников банка)"""
    if request.user.role != 'bank_employee':  # Доступ только для сотрудников банка
        return redirect('dashboard')

    applications = CreditApplication.objects.all()  # Все заявки
    return render(request, 'credits/manage_applications.html', {'applications': applications})


@login_required
def review_application(request, application_id):
    """Просмотр и принятие решения по заявке (только для сотрудников банка)"""
    if request.user.role != 'bank_employee':  # Доступ только для сотрудников банка
        return redirect('dashboard')

    application = get_object_or_404(CreditApplication, id=application_id)

    if request.method == "POST":
        form = CreditDecisionForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('manage_applications')

    else:
        form = CreditDecisionForm(instance=application)

    return render(request, 'credits/review_application.html', {'form': form, 'application': application})


@login_required
def update_application_status(request, application_id):
    """Одобрение или отклонение заявки (только для сотрудников банка)"""
    if request.user.role != 'bank_employee':  # Доступ только для сотрудников банка
        return redirect('dashboard')

    application = get_object_or_404(CreditApplication, id=application_id)

    if request.method == "POST":
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            application.status = status  # Обновляем статус заявки
            application.save()

    return redirect('manage_applications')


@login_required
def profile(request):
    """Профиль клиента, загрузка паспорта"""
    client, created = Client.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PassportUploadForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()  # Сохраняем загруженный паспорт
            return redirect("profile")  # Перенаправляем на текущую страницу

    else:
        form = PassportUploadForm(instance=client)

    return render(request, "credits/profile.html", {"form": form, "client": client})
