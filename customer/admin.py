from django.contrib import admin
from customer.models import Customer, CustomerLedger


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'father_name', 'cnic', 'mobile', 'alternate_mobile', 'resident',
        'address', 'city', 'date'
    )


class CustomerLegerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'debit_amount', 'credit_amount', 'details', 'date'
    )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerLedger, CustomerLegerAdmin)
