from django import forms
from banking_system.models import Bank, BankDetail


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'


class BankDetailForm(forms.ModelForm):
    class Meta:
        model = BankDetail
        fields = '__all__'
