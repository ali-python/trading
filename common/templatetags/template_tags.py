from django import template

from product.models import Product

register = template.Library()


@register.simple_tag
def get_products():
    products = Product.objects.all()
    return products
