from sales.views import (
    InvoiceListView, CreateInvoiceTemplateView, ProductListAPIView,
    GenerateInvoiceAPIView, InvoiceDetailTemplateView, InvoiceInstallmentListView,
    InvoiceInstallmentFormView, InvoiceInstallmentDeleteView
)
from django.urls import path

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name='invoice_list'),
    path("invoice/create", CreateInvoiceTemplateView.as_view(), name='invoice_create'),
    path("invoice/<int:pk>/detail", InvoiceDetailTemplateView.as_view(), name='invoice_detail'),
    path("product/list/api/", ProductListAPIView.as_view(), name='product_list_api'),
    path("generate/invoice/api/", GenerateInvoiceAPIView.as_view(), name='generate_invoice_api'),

    path(
        "invoice/<int:invoice_id>/installments",
        InvoiceInstallmentListView.as_view(),
        name='installment_list'
    ),

    path(
        "invoice/<int:invoice_id>/installment/add",
        InvoiceInstallmentFormView.as_view(),
        name='installment_add'
    ),

    path(
        'installment/<int:pk>/delete',
        InvoiceInstallmentDeleteView.as_view(),
        name='installment_delete')
    ,
]
