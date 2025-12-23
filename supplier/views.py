from django.shortcuts import render,get_object_or_404
from supplier.forms import SupplierFormView,SupplierStatementFormView
from supplier.models import Supplier, SupplierStatement
from django.views.generic import ListView, FormView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from common.mixins import CustomLoginRequiredMixin

# Create your views here.

class SupplierList(CustomLoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'supplier/list_supplier.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(SupplierList,self).get_context_data(**kwargs)
        supplier_statements = SupplierStatement.objects.all()
        try:
            supplier_amounts = supplier_statements.aggregate(Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get('supplier_amount__sum') or 0
            payment_amounts = supplier_statements.aggregate(Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum') or 0
        except:
            supplier_amounts = 0
            payment_amounts = 0
        total_remaining_amount = supplier_amounts - payment_amounts
        context.update({
             'total_remaining_amount': total_remaining_amount
        })
        return context

class SupplierDelete(CustomLoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'supplier/supplier_confirm_delete.html'
    context_object_name = 'ex'
    success_url = reverse_lazy('supplier:list_supplier')


class SupplierStatementList(CustomLoginRequiredMixin, ListView):
    model = SupplierStatement
    template_name = 'supplier/list_supplier_statement.html'
    paginate_by = 100

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SupplierStatement.objects.filter(supplier_id=pk).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        supplier = get_object_or_404(Supplier, id=pk)
        statements = SupplierStatement.objects.filter(supplier=supplier)
        data = statements.aggregate(
            supplier_total=Sum('supplier_amount'),
            payment_total=Sum('payment_amount')
        )
        context.update({
            'supplier': supplier,
            'supplier_total_remaining_amount': (data['supplier_total'] or 0) - (data['payment_total'] or 0)
        })
        return context


class SupplierAdd(CustomLoginRequiredMixin,FormView):
    form_class = SupplierFormView
    template_name = 'supplier/add_supplier.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('supplier:list_supplier'))
    
    def form_invalid(self, form):
        return super(SupplierAdd, self).form_invalid(form)
    
class AddSupplierStatement(CustomLoginRequiredMixin, FormView):
    form_class = SupplierStatementFormView
    template_name = 'supplier/add_supplier_statement.html'

    def form_valid(self, form):
        obj = form.save(commit=False) 
        obj.supplier = get_object_or_404(Supplier, id=self.kwargs.get('pk'))
        obj.save()
        return HttpResponseRedirect(reverse(
            'supplier:list_supplier_statement',
            kwargs={'pk': obj.supplier.id}
        ))

    def form_invalid(self, form):
        print(form.errors)
        return super(AddSupplierStatement, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = get_object_or_404(Supplier, id=self.kwargs.get('pk'))
        context.update({
            'supplier': supplier
        })
        return context
    
class SupplierStatementUpdate(CustomLoginRequiredMixin, UpdateView):
    model = SupplierStatement
    form_class = SupplierStatementFormView
    template_name = 'supplier/update_supplier_statement.html'
    context_object_name = 'form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.supplier is None:
            raise ValueError("Supplier is missing for this statement")
        obj.save()
        return HttpResponseRedirect(
            reverse('supplier:list_supplier_statement', kwargs={'pk': obj.supplier.id})
        )

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SupplierStatementUpdate, self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(supplier__id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context
  
class StatementPayment(CustomLoginRequiredMixin, FormView):
    form_class = SupplierStatementFormView
    template_name = 'supplier/payment.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            StatementPayment, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse(
            'supplier:list_supplier_statement', kwargs={
                'pk': self.kwargs.get('pk')}))

    def form_invalid(self, form):
        return super(StatementPayment, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StatementPayment, self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context