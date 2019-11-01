from django.db import models
from django.utils import timezone


class Bank(models.Model):
    name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200, null=True, blank=True)
    account_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BankDetail(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank_detail',
                             null=True, blank=True)
    debit = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                null=True, blank=True)
    credit = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                 null=True, blank=True)
    amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                 null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    # def __str__(self):
    #     return self.bank.name
