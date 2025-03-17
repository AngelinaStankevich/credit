from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()


class CreditApplication(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # срок в месяцах
    status = models.CharField(max_length=20, choices=[('pending', 'На рассмотрении'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
