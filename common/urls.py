from .views import IndexView, MonthlyReports
from common.stock_logs import DailyStockLogs, MonthlyStockLogs
from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('reports/monthly', MonthlyReports.as_view(), name='reports'),
    path('logs/daily', DailyStockLogs.as_view(), name='daily_logs'),
    path('logs/monthly', MonthlyStockLogs.as_view(), name='monthly_logs')
]
