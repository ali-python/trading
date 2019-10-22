from django import forms
from sales.models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = ''
        fields = '__all__'
