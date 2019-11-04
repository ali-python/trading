from django.shortcuts import render
from expense.forms import ExpenseFormView
from expense.models import Expense
from django.views.generic import ListView, FormView, DeleteView, UpdateView
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
    ordering = '-id'

    def get_queryset(self):
        queryset = self.queryset

        if not queryset:
            queryset = Expense.objects.all().order_by('-id')

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                date__icontains=self.request.GET.get('date')
            )

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(ExpenseList, self).get_context_data(**kwargs)
    #     expense = (
    #         Expense.objects.all()
    #     )
    #     context.update({
    #         'expense': expense
    #     })
    #     return context


class UpdateExpense(UpdateView):
    model = Expense
    form_class = ExpenseFormView
    template_name = 'expense/update_expense.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('expense:list'))

    def form_invalid(self, form):
        return super(UpdateExpense, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateExpense, self).get_context_data(**kwargs)
        expense = Expense.objects.all()
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
