from django.shortcuts import render
from django.views.generic import ListView

from sales.models import Invoice


class InvoiceListView(ListView):
    template_name = 'sales/invoice_list.html'
    model = Invoice
    paginate_by = 100
    ordering = '-id'

