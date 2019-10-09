from django.urls import path
from product.views import (
    AddProduct, AddProductDetail, UpdateProduct, ProductList,
    StockInProduct, StockOutProduct, StockDetail
)

urlpatterns = [
    path('add/', AddProduct.as_view(), name='add'),
    path('add/detail/',AddProductDetail.as_view(), name='add_detail'),
    path('list/', ProductList.as_view(), name='list'),
    path('update/<int:pk>/', UpdateProduct.as_view(), name='update'),
    path('stock/item/<int:pk>/add', StockInProduct.as_view(), name='add_stock'),
    path('stock/item/<int:pk>/out', StockOutProduct.as_view(), name='stock_out'),
    path('stock/item/<int:pk>/detail', StockDetail.as_view(), name='stock_detail'),

]