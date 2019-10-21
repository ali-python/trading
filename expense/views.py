from django.shortcuts import render
from expense.forms import ExpenseFormView
from expense.models import Expense
from django.views.generic import ListView, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


class AddExpense(FormView):
    form_class = ExpenseFormView
    template_name = 'expense/add_expense.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('expense:list'))

    def form_invalid(self, form):
        return super(AddExpense, self).form_invalid(form)


class ExpenseList(ListView):
    template_name = 'expense/expense_list.html'
    model = Expense
    paginate_by = 100
    is_paginated = True

    def get_context_data(self, **kwargs):
        context = super(ExpenseList, self).get_context_data(**kwargs)
        expense = (
            Expense.objects.all()
        )
        context.update({
            'expense': expense
        })
        return context


class DeleteExpense(DeleteView):
    model = Expense
    success_url = reverse_lazy('expense:list')
    success_message = ''

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
