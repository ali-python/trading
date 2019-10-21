from django.urls import path
from expense.views import (
    AddExpense, ExpenseList, DeleteExpense
)

urlpatterns = [
    path('add/', AddExpense.as_view(), name='add'),
    path('list/', ExpenseList.as_view(), name='list'),
    path('delete/<int:pk>/', DeleteExpense.as_view(), name='delete'),

]