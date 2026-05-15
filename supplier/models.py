from django.db import models
from django.db.models import Sum
from decimal import Decimal
# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name or ''

    def supplier_remaining_amount(self):
        data = self.statements.all().aggregate(
            total_amount=Sum('supplier_amount'),
            total_payments=Sum('payment_amount')
        )
        total_amount = data['total_amount'] or 0
        total_payments = data['total_payments'] or 0
        return total_amount - total_payments
    
class SupplierStatement(models.Model):
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,related_name='statements', blank=True, null=True)
    supplier_amount = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    payment_amount = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    description = models.TextField(max_length=200, blank=True, null=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.supplier.name if self.supplier else ''
    
    @property
    def remaining_amount(self):
        supplier_amount = self.supplier_amount or Decimal('0.00')
        payment_amount = self.payment_amount or Decimal('0.00')
        return supplier_amount - payment_amount