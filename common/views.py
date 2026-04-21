from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from sales.models import Invoice
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import datetime
from customer.models import Customer
from product.models import StockOut, Product,StockIn,PurchasedItem
from expense.models import Expense
from supplier.models import Supplier, SupplierStatement
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect,HttpResponse
from common.models import AdminConfiguration
from django.contrib.auth import authenticate



class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # register new user in the system
        user = form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        auth_user = authenticate(username=username, password=raw_password)
        auth_login(self.request, auth_user)

        return HttpResponseRedirect(reverse('common:login'))

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):       
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context.update({
                'username': self.request.POST.get('username'),
                'password1': self.request.POST.get('password1'),
                'password2': self.request.POST.get('password2')
            })

        return 

class LoginView(FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        try:
            admin_config = AdminConfiguration.objects.get(id=1)
            context.update({
                'config': admin_config
            })
        except AdminConfiguration.DoesNotExist:
            pass
        return context


class LogoutView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('common:login'))

class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        today = timezone.now().date()

        # -------------------------
        # TODAY DATA
        # -------------------------
        today_invoices = Invoice.objects.filter(date=today)

        today_sales_count = today_invoices.count()

        today_revenue = today_invoices.aggregate(
            total=Sum('grand_total')
        )['total'] or 0

        today_cost = PurchasedItem.objects.filter(
            invoice__date=today
        ).aggregate(
            total=Sum('purchase_amount')
        )['total'] or 0

        today_expenses = Expense.objects.filter(date=today).aggregate(
            total=Sum('amount')
        )['total'] or 0

        today_profit = float(today_revenue) - float(today_cost) - float(today_expenses)

        # -------------------------
        # PRODUCT STOCK
        # -------------------------
        all_products = list(Product.objects.all())

        low_stock_products = [
            p for p in all_products
            if 0 < p.product_available_items() <= float(p.notify_qty or 0)
        ]

        out_of_stock = [
            p for p in all_products
            if p.product_available_items() <= 0
        ]

        # -------------------------
        # GENERAL STATS
        # -------------------------
        total_customers = Customer.objects.count()
        total_suppliers = Supplier.objects.count()
        total_products = len(all_products)

        supplier_agg = SupplierStatement.objects.aggregate(
            total_amount=Sum('supplier_amount'),
            total_paid=Sum('payment_amount')
        )

        total_supplier_balance = float(supplier_agg['total_amount'] or 0) - float(supplier_agg['total_paid'] or 0)

        total_receivable = Invoice.objects.aggregate(
            total=Sum('remaining_payment')
        )['total'] or 0

        # -------------------------
        # MONTHLY DATA
        # -------------------------
        month_start = today.replace(day=1)

        monthly_revenue = Invoice.objects.filter(date__gte=month_start).aggregate(
            total=Sum('grand_total')
        )['total'] or 0

        monthly_cost = PurchasedItem.objects.filter(
            invoice__date__gte=month_start
        ).aggregate(
            total=Sum('purchase_amount')
        )['total'] or 0

        monthly_expenses = Expense.objects.filter(date__gte=month_start).aggregate(
            total=Sum('amount')
        )['total'] or 0

        monthly_profit = float(monthly_revenue) - float(monthly_cost) - float(monthly_expenses)

        # -------------------------
        # LAST 7 DAYS CHART
        # -------------------------
        last_7_days = []
        last_7_sales = []
        last_7_profit = []

        for i in range(6, -1, -1):
            day = today - datetime.timedelta(days=i)

            day_revenue = Invoice.objects.filter(date=day).aggregate(
                total=Sum('grand_total')
            )['total'] or 0

            day_cost = PurchasedItem.objects.filter(
                invoice__date=day
            ).aggregate(
                total=Sum('purchase_amount')
            )['total'] or 0

            day_expense = Expense.objects.filter(date=day).aggregate(
                total=Sum('amount')
            )['total'] or 0

            last_7_days.append(day.strftime('%d %b'))
            last_7_sales.append(float(day_revenue))

            last_7_profit.append(
                float(day_revenue) - float(day_cost) - float(day_expense)
            )

        # -------------------------
        # RECENT INVOICES
        # -------------------------
        recent_invoices = Invoice.objects.filter(date=today)\
            .select_related('customer')\
            .order_by('-id')[:10]

        # -------------------------
        # CONTEXT
        # -------------------------
        context.update({
            'today': today,

            'today_sales_count': today_sales_count,
            'today_revenue': today_revenue,
            'today_expenses': today_expenses,
            'today_profit': today_profit,

            'total_products': total_products,
            'low_stock_products': low_stock_products[:5],
            'low_stock_count': len(low_stock_products),
            'out_of_stock_count': len(out_of_stock),

            'total_customers': total_customers,
            'total_suppliers': total_suppliers,
            'total_supplier_balance': total_supplier_balance,
            'total_receivable': total_receivable,

            'monthly_revenue': monthly_revenue,
            'monthly_expenses': monthly_expenses,
            'monthly_profit': monthly_profit,

            'last_7_days': last_7_days,
            'last_7_sales': last_7_sales,
            'last_7_profit': last_7_profit,

            'recent_invoices': recent_invoices,
        })

        return context

class MonthlyReports(TemplateView):
    template_name = 'reports/reports.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            MonthlyReports, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MonthlyReports, self).get_context_data(**kwargs)
        data_result = []
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
               'date': start_month.strftime('%b-%y')
            })
            data_result.append(data)

        context.update({
            'results': data_result
        })
        return context
