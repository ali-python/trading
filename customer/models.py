from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    cnic = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    alternate_mobile = models.CharField(max_length=200, null=True, blank=True)
    resident = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomerLedger(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='customer_ledger'
    )
    invoice = models.ForeignKey(
        'sales.Invoice', related_name='invoice_ledger', blank=True, null=True, on_delete=models.CASCADE
    )
    debit_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    credit_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    details = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.customer.name
