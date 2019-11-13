from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Bank(models.Model):
    name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200, null=True, blank=True)
    account_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def bank_balance(self):
        bank_details = self.bank_detail.all()
        if bank_details:
            debit = bank_details.aggregate(Sum('debit'))
            credit = bank_details.aggregate(Sum('credit'))

            debit_amount = debit.get('debit__sum')
            credit_amount = credit.get('credit__sum')
        else:
            debit_amount = 0
            credit_amount = 0

        balance = credit_amount - debit_amount
        return balance


class BankDetail(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank_detail',
                             null=True, blank=True)
    invoice = models.ForeignKey(
        'sales.Invoice', related_name='bank_invoice'
        , null=True, blank=True, on_delete=models.SET_NULL
    )
    debit = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                null=True, blank=True)
    credit = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                 null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.bank.name if self.bank else ''
