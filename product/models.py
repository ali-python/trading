from django.db import models
from django.utils import timezone
from django.db.models import Sum


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='product_detail')
    category = models.CharField(max_length=200, null=True, blank=True)
    litre = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                null=True, blank=True)
    quantity = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                   null=True, blank=True)
    unit_price = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                     null=True, blank=True)
    amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                 null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.product)

    def total_items(self):
        try:
            obj_stock_in = self.product_stockin.aggregate(Sum('stock_quantity'))
            stock_in = float(obj_stock_in.get('stock_quantity__sum'))
        except:
            stock_in = 0

        return stock_in

    def product_available_items(self):
        try:
            obj_stock_in = self.product_stockin.aggregate(Sum('stock_quantity'))
            stock_in = float(obj_stock_in.get('stock_quantity__sum'))
        except:
            stock_in = 0
        try:
            obj_stock_out = self.product_stockout.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0

        return stock_in - stock_out


class StockIn(models.Model):
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='product_stockin')
    stock_quantity = models.CharField(max_length=200, null=True, blank=True)
    price_per_item = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                         null=True, blank=True)
    total_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.product)


class StockOut(models.Model):
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='product_stockout')
    stock_out_quantity = models.DecimalField(max_digits=65, decimal_places=2,
                                             default=0, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.product)
