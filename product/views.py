from django.shortcuts import render
from product.forms import (
    ProductForm, ProductDetailForm, StockInForm, StockOutForm
)
from product.models import (
    Product, ProductDetail
)
from django.views.generic import ListView, FormView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AddProduct(FormView):
    form_class = ProductForm
    template_name = 'product/add_product.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:add_detail'))

    def form_invalid(self, form):
        return super(AddProduct, self).form_invalid(form)


class AddProductDetail(FormView):
    form_class = ProductDetailForm
    template_name = 'product/add_product_detail.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(AddProductDetail, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddProductDetail, self).get_context_data(**kwargs)
        product = Product.objects.all()
        context.update({
            'products': product
        })
        return context


class UpdateProduct(UpdateView):
    model = ProductDetail
    form_class = ProductDetailForm
    template_name = 'product/update_product.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(UpdateProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateProduct, self).get_context_data(**kwargs)
        product = Product.objects.all()
        context.update({
            'products': product
        })
        return context


class ProductList(ListView):
    model = ProductDetail
    template_name = 'product/product_list.html'
    paginate_by = 100
    is_paginated = True
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        detail = ProductDetail.objects.all()
        context.update({
            'details': detail
        })
        return context


class StockInProduct(FormView):
    form_class = StockInForm
    template_name = 'product/add_stock_item.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(StockInProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StockInProduct, self).get_context_data(**kwargs)
        try:
            product = (
                ProductDetail.objects.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found')
        context.update({
            'products': product
        })
        return context


class StockOutProduct(FormView):
    form_class = StockOutForm
    template_name = 'product/stock_out_product.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(StockOutProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StockOutProduct, self).get_context_data(**kwargs)

        try:
            product = (
                ProductDetail.objects.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found')

        context.update({
            'products': product
        })
        return context


class StockDetail(ListView):
    template_name = 'product/stock_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StockDetail, self).get_context_data(**kwargs)

        try:
            item = (
                ProductDetail.objects.get(id=self.kwargs.get('pk'))
            )
        except StockInProduct.DoesNotExist:
            return Http404('Item does not exists in database')

        item_stock_in = item.product_stockin.all()
        item_stock_out = item.product_stockout.all()

        context.update({
            'item': item,
            'item_stock_in': item_stock_in.order_by('-date'),
            'item_stock_out': item_stock_out.order_by('-date')
        })

        return context
