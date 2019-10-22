from sales.views import InvoiceListView
from django.urls import path

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name='invoice_list'),
]
