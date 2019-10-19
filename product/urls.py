from django.urls import path
from product.views import (
    AddProductCategory, AddProduct, UpdateProduct, ProductList,
    StockInProduct, StockOutProduct, StockInDetail, StockOutDetail
)

urlpatterns = [
    path('add/', AddProduct.as_view(), name='add'),
    path('add/category/',AddProductCategory.as_view(), name='add_category'),
    path('list/', ProductList.as_view(), name='list'),
    path('update/<int:pk>/', UpdateProduct.as_view(), name='update'),
    path('stock/item/<int:pk>/add', StockInProduct.as_view(), name='add_stock'),
    path('stock/item/<int:pk>/out', StockOutProduct.as_view(), name='stock_out'),
    path('stockin/item/<int:pk>/detail', StockInDetail.as_view(), name='stockin_detail'),
    path('stockout/item/<int:pk>/detail', StockOutDetail.as_view(), name='stockout_detail'),

]