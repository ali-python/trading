from django.contrib import admin
from sales.models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'invoice', 'total_quantity', 'sub_total', 'grand_total', 'date'
    )

    @staticmethod
    def invoice(obj):
        return str(obj.id).zfill(7)


admin.site.register(Invoice, InvoiceAdmin)
