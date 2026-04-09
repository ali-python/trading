from django import forms
from supplier.models import Supplier,SupplierStatement

class SupplierFormView(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierStatementFormView(forms.ModelForm):
    class Meta:
        model = SupplierStatement
        fields = ['supplier_amount', 'payment_amount', 'description', 'date']