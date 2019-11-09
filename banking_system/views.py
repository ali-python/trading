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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddBankFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('bank:list'))

    def form_invalid(self, form):
        return super(AddBankFormView, self).form_invalid(form)


class BankListView(ListView):
    model = Bank
    template_name = 'banking/bank_list.html'
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            BankListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Bank.objects.all().order_by('-id')

        if self.request.GET.get('bank_name'):
            queryset = queryset.filter(
                name__contains=self.request.GET.get('bank_name'))

        if self.request.GET.get('account_no'):
            queryset = queryset.filter(
                account_number=self.request.GET.get('account_no').lstrip('0')
            )

        return queryset.order_by('-id')

    # def get_context_data(self, **kwargs):
    #     context = super(BankListView, self).get_context_data(**kwargs)
    #     bank = Bank.objects.all()
    #     context.update({
    #         'bank': bank
    #     })
    #     return context


class AddBankUpdateView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'banking/update_add_bank_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddBankUpdateView, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            BankDetailListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = self.queryset
        if not queryset:
            queryset = self.model.objects.filter(
                bank__id=self.kwargs.get('pk')).order_by('-date')

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                date__icontains=self.request.GET.get('date')
            )

        return queryset

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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DebitBankFormView, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DebitBankUpdateView, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CreditBankFormView, self).dispatch(request, *args, **kwargs)


class CreditBankUpdateView(DebitBankUpdateView):
    template_name = 'banking/update_credit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CreditBankUpdateView, self).dispatch(request, *args, **kwargs)
