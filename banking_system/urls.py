from django.urls import path
from banking_system.views import (
    AddBankFormView, BankListView, BankDetailListView, AddBankUpdateView,
    CreditBankFormView, CreditBankUpdateView, DebitBankFormView, DebitBankUpdateView
)

urlpatterns = [
    path('add/', AddBankFormView.as_view(), name='add'),
    path('list/', BankListView.as_view(), name='list'),
    path('detail_list/<int:pk>/', BankDetailListView.as_view(), name='detail_list'),
    path('update/<int:pk>/', AddBankUpdateView.as_view(), name='update'),
    path('credit/<int:pk>/', CreditBankFormView.as_view(), name='credit'),
    path('credit/update/<int:pk>/', CreditBankUpdateView.as_view(), name='credit_update'),
    path('debit/<int:pk>/', DebitBankFormView.as_view(), name='debit'),
    path('debit/update/<int:pk>/', DebitBankUpdateView.as_view(), name='debit_update'),

]