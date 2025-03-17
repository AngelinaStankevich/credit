from django.contrib import admin
from .models import CreditApplication


class CreditApplicationAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'duration', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('client__user__username',)
    actions = ['approve_applications', 'reject_applications']

    @admin.action(description="Одобрить выбранные заявки")
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Отклонить выбранные заявки")
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')


admin.site.register(CreditApplication, CreditApplicationAdmin)
