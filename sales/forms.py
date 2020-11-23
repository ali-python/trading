from django import forms
from sales.models import Invoice, InvoiceInstallment


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceInstallmentForm(forms.ModelForm):
    class Meta:
        model = InvoiceInstallment
        fields = '__all__'
