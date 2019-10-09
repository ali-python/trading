from django.contrib import admin
from product.models import Product, ProductDetail, StockIn, StockOut


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date'
    )


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category', 'litre', 'quantity', 'unit_price', 'amount', 'date'
    )


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category', 'stock_quantity', 'price_per_item',
        'total_amount', 'date'
    )

    @staticmethod
    def category(obj):
        return obj.ProductDetail.category


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category', 'stock_out_quantity', 'date'
    )

    @staticmethod
    def category(obj):
        return obj.ProductDetail.category


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
