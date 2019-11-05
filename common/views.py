from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from sales.models import Invoice
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import datetime
from customer.models import Customer
from product.models import StockOut
from django.http import HttpResponseRedirect
from django.urls import reverse


class IndexView(TemplateView):
    template_name = 'index.html'


class MonthlyReports(TemplateView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        context = super(MonthlyReports, self).get_context_data(**kwargs)
        data_result = []
        last_total = 0
        for month in range(60):
            data = {}
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            invoice = Invoice.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if invoice.exists():
                commission = invoice.aggregate(
                    Sum('grand_total'))
                grand_total = float(
                    commission.get('grand_total__sum') or 0
                )

            else:
                grand_total = 0

            if invoice.exists():
                cash_payment = invoice.aggregate(
                    Sum('cash_payment'))
                total_cash_payment = float(
                    cash_payment.get(
                        'cash_payment__sum') or 0
                )
            else:
                total_cash_payment = 0

            if invoice.exists():
                quantity = invoice.aggregate(
                    Sum('total_quantity'))
                total_quantity = float(
                    quantity.get(
                        'total_quantity__sum') or 0
                )
            else:
                total_quantity = 0

            customer = Customer.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if customer.exists():
                total_customer = customer.count()

            else:
                total_customer = 0

            data.update({
               'grand_total': grand_total,
               'total_cash_payment': total_cash_payment,
               'total_quantity': total_quantity,
               'total_customer': total_customer,
               'date': start_month.strftime('%B, %Y')
            })
            data_result.append(data)

        context.update({
            'results': data_result
        })
        return context
