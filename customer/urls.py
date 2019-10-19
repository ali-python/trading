from django.urls import path
from customer.views import (
    AddCustomer, CustomerList, UpdateCustomer
)

urlpatterns = [
    path('add/', AddCustomer.as_view(), name='add'),
    path('list/', CustomerList.as_view(), name='list'),
    path('update/<int:pk>/', UpdateCustomer.as_view(), name='update'),

]