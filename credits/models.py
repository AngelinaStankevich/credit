from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('bank_employee', 'Сотрудник банка'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')


class Client(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)  # Ссылка на кастомную модель пользователя
    passport_scan = models.FileField(upload_to="passports/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class CreditApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="applications")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()  # Срок в месяцах
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка {self.id} - {self.get_status_display()}"
