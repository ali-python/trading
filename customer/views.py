from django.shortcuts import render
from django.views.generic import ListView, FormView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from customer.models import Customer
from customer.forms import CustomerForm


class AddCustomer(FormView):
    form_class = CustomerForm
    template_name = 'customer/add_customer.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('customer:list'))

    def form_invalid(self, form):
        return super(AddCustomer, self).form_invalid(form)


class CustomerList(ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    paginate_by = 100
    is_paginated = True
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data(**kwargs)
        customer = Customer.objects.all()
        context.update({
            'customer': customer
        })
        return context


class UpdateCustomer(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/update_customer.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('customer:list'))

    def form_invalid(self, form):
        return super(UpdateCustomer, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateCustomer, self).get_context_data(**kwargs)
        customer = Customer.objects.all()
        context.update({
            'customer': customer
        })
        return context
