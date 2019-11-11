from django.contrib import admin
from banking_system.models import BankDetail, Bank


class BankAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'branch', 'account_number'
    )


class BankDetailAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'debit', 'credit', 'invoice', 'description', 'date'
    )


admin.site.register(Bank, BankAdmin)
admin.site.register(BankDetail, BankDetailAdmin)
