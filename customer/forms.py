from django import forms
from customer.models import Customer, CustomerLedger


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerLedgerForm(forms.ModelForm):
    class Meta:
        model = CustomerLedger
        fields = '__all__'
