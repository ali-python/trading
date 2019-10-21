from django.contrib import admin
from product.models import ProductCategory, Product, StockIn, StockOut


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category', 'date'
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'name', 'category', 'litre', 'quantity', 'unit_price', 'amount', 'date'
    )

    @staticmethod
    def category(obj):
        return obj.ProductCategory.category


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category_name', 'stock_quantity', 'price_per_item',
        'total_amount', 'buying_price_item', 'total_buying_amount', 'dated_order'
    )

    @staticmethod
    def category_name(obj):
        return obj.product.category


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category', 'stock_out_quantity', 'selling_price', 'buying_price', 'date'
    )

    @staticmethod
    def category(obj):
        return obj.product.category


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)