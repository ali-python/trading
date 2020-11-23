import json
from django.core.paginator import Paginator
from django.views.generic import (
    ListView, TemplateView, View, FormView, DeleteView)
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.shortcuts import render
from customer.models import Customer
from product.models import Product
from sales.models import Invoice, InvoiceInstallment
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from customer.forms import CustomerForm, CustomerLedgerForm
from product.forms import ProductForm, StockOutForm, PurchasedItemForm
from sales.forms import InvoiceForm, InvoiceInstallmentForm
from banking_system.models import Bank
from banking_system.forms import BankDetailForm


class InvoiceListView(ListView):
    template_name = 'sales/invoice_list.html'
    model = Invoice
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            InvoiceListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Invoice.objects.all().order_by('-id')

        if self.request.GET.get('customer_name'):
            queryset = queryset.filter(
                customer__name__contains=self.request.GET.get('customer_name'))

        if self.request.GET.get('customer_id'):
            queryset = queryset.filter(
                id=self.request.GET.get('customer_id').lstrip('0')
            )

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                date=self.request.GET.get('date')
            )

        return queryset.order_by('-id')


class CreateInvoiceTemplateView(TemplateView):
    template_name = 'sales/create_invoice.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CreateInvoiceTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateInvoiceTemplateView, self).get_context_data(**kwargs)
        context.update({
            'customers': Customer.objects.all().order_by('name'),
            'products': Product.objects.all().order_by('name'),
            'today_date': timezone.now().date(),
            'banks': Bank.objects.all().order_by('name')
        })
        return context


class ProductListAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ProductListAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        items = []

        for product in products:
            p = {
                'id': product.id,
                'name': product.name,
                'category_name': product.category.category,
            }

            if product.stockin_product.exists():
                stock_detail = product.stockin_product.all().latest('id')
                p.update({
                    'selling_price': '%g' % stock_detail.price_per_item,
                    'buying_price': '%g' % stock_detail.buying_price_item,
                })

                all_stock = product.stockin_product.all()
                if all_stock:
                    all_stock = all_stock.aggregate(Sum('stock_quantity'))
                    all_stock = float(all_stock.get('stock_quantity__sum') or 0)
                else:
                    all_stock = 0

                purchased_stock = product.stockout_product.all()
                if purchased_stock:
                    purchased_stock = purchased_stock.aggregate(
                        Sum('stock_out_quantity'))
                    purchased_stock = float(
                        purchased_stock.get('stock_out_quantity__sum') or 0)
                else:
                    purchased_stock = 0

                p.update({
                    'stock': all_stock - purchased_stock
                })

            else:
                p.update(
                    {
                        'selling_item': 0,
                        'buying_price': 0
                    }
                )

            items.append(p)

        return JsonResponse({'products': items})


class GenerateInvoiceAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            GenerateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        customer_name = self.request.POST.get('customer_name')
        customer_phone = self.request.POST.get('customer_phone')
        customer_cnic = self.request.POST.get('customer_cnic')
        sub_total = self.request.POST.get('sub_total')
        discount = self.request.POST.get('discount')
        shipping = self.request.POST.get('shipping')
        grand_total = self.request.POST.get('grand_total')
        totalQty = self.request.POST.get('totalQty')
        remaining_payment = self.request.POST.get('remaining_amount')
        paid_amount = self.request.POST.get('paid_amount')
        cash_payment = self.request.POST.get('cash_payment')
        returned_cash = self.request.POST.get('returned_cash')
        payment_type = self.request.POST.get('payment_type')
        bank = self.request.POST.get('bank')
        items = json.loads(self.request.POST.get('items'))

        with transaction.atomic():
            invoice_form_kwargs = {
                'discount': discount,
                'grand_total': grand_total,
                'total_quantity': totalQty,
                'shipping': shipping,
                'paid_amount': paid_amount,
                'remaining_payment': remaining_payment,
                'cash_payment': cash_payment,
                'returned_payment': returned_cash,
                'payment_type': payment_type,
            }
            invoice_form = InvoiceForm(invoice_form_kwargs)
            invoice = invoice_form.save()

            if self.request.POST.get('customer_id'):
                customer_id = self.request.POST.get('customer_id')
                customer = Customer.objects.get(id=customer_id)
            else:
                customer_form_kwargs = {
                    'name': customer_name,
                    'cnic': customer_cnic,
                    'mobile': customer_phone,
                }
                customer_form = CustomerForm(customer_form_kwargs)
                if customer_form.is_valid():
                    customer = customer_form.save()
                    customer_id = customer.id
                else:
                    customer_id = ''

            if customer_id:
                invoice.customer = customer
                invoice.save()

            for item in items:
                product = Product.objects.get(id=item.get('item_id'))
                latest_stockin = product.stockin_product.all().latest('id')

                stock_out_kwargs = {
                    'product': product.id,
                    'invoice': invoice.id,
                    'stock_out_quantity': float(item.get('qty')),
                    'buying_price': (
                            float(latest_stockin.buying_price_item) *
                            float(item.get('qty'))),
                    'selling_price': (
                            float(item.get('price')) * float(item.get('qty'))),
                    'date': timezone.now().date()
                }
                stock_out = StockOutForm(stock_out_kwargs)
                stock_out.save()

                purchased_item_kwargs = {
                    'item': product.id,
                    'invoice': invoice.id,
                    'quantity': item.get('qty'),
                    'price': item.get('price'),
                    'purchase_amount': item.get('total'),
                }
                purchase_item = PurchasedItemForm(purchased_item_kwargs)
                purchase_item.save()

            if customer_id or self.request.POST.get('customer_id'):
                if payment_type == 'Installment':
                    installment_kwargs = {
                        'invoice': invoice.id,
                        'paid_amount': paid_amount,
                        'description': 'Advance Payment'

                    }
                    installment__form = InvoiceInstallmentForm(
                        installment_kwargs)
                    installment__form.save()

                elif float(remaining_payment):

                    ledger_form_kwargs = {
                        'customer': customer_id,
                        'invoice': invoice.id,
                        'debit_amount': remaining_payment,
                        'details': (
                                'Remaining Payment for Bill/Receipt No %s '
                                % str(invoice.id).zfill(7)),
                        'date': timezone.now()
                    }

                    customer_ledger = CustomerLedgerForm(ledger_form_kwargs)
                    customer_ledger.save()

            if payment_type == 'Check':
                bank_details_kwargs = {
                    'bank': bank,
                    'invoice': invoice.id,
                    'credit': paid_amount,
                    'description': 'Invoice Payment is by Check/Bank.'
                }
                bank_details_form = BankDetailForm(bank_details_kwargs)
                bank_details = bank_details_form.save()
                invoice.bank = bank_details.bank
                invoice.save()

        return JsonResponse({'invoice_id': invoice.id})


class InvoiceDetailTemplateView(TemplateView):
    template_name = 'sales/invoice_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            InvoiceDetailTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailTemplateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'invoice': invoice
        })
        return context


class InvoiceInstallmentListView(ListView):
    model = InvoiceInstallment
    template_name = 'sales/installment_list.html'
    paginate_by = 100
    ordering = '-date'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            InvoiceInstallmentListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = InvoiceInstallment.objects.filter(
            invoice=self.kwargs.get('invoice_id'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            InvoiceInstallmentListView, self).get_context_data(**kwargs)

        invoice = Invoice.objects.get(id=self.kwargs.get('invoice_id'))
        invoice_installments = InvoiceInstallment.objects.filter(
            invoice__id=invoice.id)


        grand_total = invoice.grand_total

        if invoice_installments.exists():
            total_paid_amount = invoice_installments.aggregate(
                Sum('paid_amount'))
            total_paid_amount = float(
                total_paid_amount.get('paid_amount__sum') or 0
            )

        else:
            total_paid_amount = 0

        context.update({
            'invoice_id': self.kwargs.get('invoice_id'),
            'total_paid_amount': total_paid_amount,
            'remaining_amount': float(grand_total) - total_paid_amount
        })
        return context


class InvoiceInstallmentFormView(FormView):
    form_class = InvoiceInstallmentForm
    template_name = 'sales/installment_add.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(
            reverse('sales:installment_list',
                    kwargs={'invoice_id': self.kwargs.get('invoice_id')}))

    def form_invalid(self, form):
        return super(InvoiceInstallmentFormView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            InvoiceInstallmentFormView, self).get_context_data(**kwargs)
        context.update({
            'invoice': Invoice.objects.get(id=self.kwargs.get('invoice_id'))
        })
        return context


class InvoiceInstallmentDeleteView(DeleteView):
    model = InvoiceInstallment
    success_message = ''

    def __init__(self, *args, **kwargs):
        super(InvoiceInstallmentDeleteView, self).__init__(*args, **kwargs)
        self.invoice_id = None

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        installment = InvoiceInstallment.objects.get(id=self.kwargs.get('pk'))
        self.invoice_id = installment.invoice.id

        return super(
            InvoiceInstallmentDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'sales:installment_list', kwargs={'invoice_id': self.invoice_id})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
