from django import forms
from product.models import (
    Product, ProductDetail, StockIn, StockOut
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = '__all__'


class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = '__all__'


class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = '__all__'
