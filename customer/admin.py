from django.contrib import admin
from customer.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'father_name', 'cnic', 'mobile', 'alternate_mobile', 'resident',
        'address', 'city', 'date'
    )


admin.site.register(Customer, CustomerAdmin)
