from sales.views import InvoiceListView, CreateInvoiceTemplateView, ProductListAPIView, GenerateInvoiceAPIView, InvoiceDetailTemplateView
from django.urls import path

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name='invoice_list'),
    path("invoice/create", CreateInvoiceTemplateView.as_view(), name='invoice_create'),
    path("invoice/<int:pk>/detail", InvoiceDetailTemplateView.as_view(), name='invoice_detail'),
    path("product/list/api/", ProductListAPIView.as_view(), name='product_list_api'),
    path("generate/invoice/api/", GenerateInvoiceAPIView.as_view(), name='generate_invoice_api'),
]
