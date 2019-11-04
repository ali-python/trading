from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from datetime import datetime
from customer.models import Customer
from product.models import StockOut


class IndexView(TemplateView):
    template_name = 'index.html'


class MonthlyReport(TemplateView):
    template_name = 'reports/monthly_report.html'
