from django.shortcuts import render
from banking_system.forms import BankForm, BankDetailForm
from banking_system.models import Bank, BankDetail
from django.views.generic import ListView, FormView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AddBankFormView(FormView):
    form_class = BankForm
    template_name = 'banking/add_bank.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('bank:list'))

    def form_invalid(self, form):
        return super(AddBankFormView, self).form_invalid(form)


class AddBankListView(ListView):
    model = Bank
    template_name = 'banking/add_bank_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(AddBankListView, self).get_context_data(**kwargs)
        bank = Bank.objects.all()
        context.update({
            'bank': bank
        })
        return context


class AddBankUpdateView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'banking/update_add_bank_list.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('bank:list'))

    def form_invalid(self, form):
        return super(AddBankUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddBankUpdateView, self).get_context_data(**kwargs)
        bank = Bank.objects.all()
        context.update({
            'bank': bank
        })
        return context


class BankDetailListView(ListView):
    model = BankDetail
    template_name = 'banking/bank_detail_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(BankDetailListView, self).get_context_data(**kwargs)

        try:
            bank = Bank.objects.get(id=self.kwargs.get('pk'))
        except Bank.DoesNotExist:
            raise Http404('Bank does not exits!')

        context.update({
            'bank': bank
        })
        return context


class DebitBankFormView(FormView):
    template_name = 'banking/debit.html'
    form_class = BankDetailForm

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse('bank:detail_list',
                                            kwargs={'pk': obj.bank.id}))

    def form_invalid(self, form):
        print(form.errors)
        print("hiiiiiii")
        return super(DebitBankFormView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            DebitBankFormView, self).get_context_data(**kwargs)
        try:
            bank = Bank.objects.get(id=self.kwargs.get('pk'))
        except Bank.DoesNotExist:
            raise Http404('Bank does not exits!')

        context.update({
            'bank': bank
        })
        return context


class DebitBankUpdateView(UpdateView):
    model = BankDetail
    form_class = BankDetailForm
    template_name = 'banking/update_debit.html'

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse('bank:detail_list',
                                            kwargs={'pk': obj.bank.id}))

    def form_invalid(self, form):
        print(form.errors)
        print('hi')
        return super(DebitBankUpdateView, self).form_invalid(form)


class CreditBankFormView(DebitBankFormView):
    template_name = 'banking/credit.html'


class CreditBankUpdateView(DebitBankUpdateView):
    template_name = 'banking/update_credit.html'
