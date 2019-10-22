from django.contrib import admin
from customer.models import Customer, CustomerLedger


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'father_name', 'cnic', 'mobile', 'alternate_mobile', 'resident',
        'address', 'city', 'date'
    )


class CustomerLegerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'debit_amount', 'credit_amount', 'invoice', 'details', 'date'
    )

    @staticmethod
    def invoice(obj):
        return str(obj.invoice.id).zfill(7) if obj.invoice else ''


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerLedger, CustomerLegerAdmin)
