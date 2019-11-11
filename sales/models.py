from django.db import models
from django.utils import timezone


class Invoice(models.Model):

    PAYMENT_CASH = 'Cash'
    PAYMENT_CHECK = 'Check'

    PAYMENT_TYPES = (
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_CHECK, 'Check'),
    )

    customer = models.ForeignKey(
        'customer.Customer',
        related_name='customer_sales',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    payment_type = models.CharField(choices=PAYMENT_TYPES, default=PAYMENT_CASH, max_length=100)

    bank_details = models.ForeignKey(
        'banking_system.Bank', related_name='bank_detail_payments',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    total_quantity = models.CharField(
        max_length=10, blank=True, null=True, default=1
    )

    sub_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    remaining_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    discount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    shipping = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    grand_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_returned = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return str(self.id).zfill(7)
