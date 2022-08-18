import json
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .functions import getCartSpec, getUserSpec, makeTransaction
from .forms import ProductModelForm


class productCreateView(CreateView):
    template_name = 'store/product_form.html'
    form_class = ProductModelForm
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(productCreateView, self).get_context_data(**kwargs)
        try:
            _, _, context['cartItems'] = getUserSpec(self.request)
            context['subject'] = 'Create'

        except (Exception, ):
            _, _, context['cartItems'] = getCartSpec(self.request)
            context['subject'] = 'Create'

        return context


class productUpdateView(UpdateView):
    template_name = 'store/product_form.html'
    form_class = ProductModelForm
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(productUpdateView, self).get_context_data(**kwargs)
        try:
            _, _, context['cartItems'] = getUserSpec(self.request)
            context['subject'] = 'Update'

        except (Exception, ):
            _, _, context['cartItems'] = getCartSpec(self.request)
            context['subject'] = 'Update'

        return context


class productListView(ListView):
    template_name = 'store/store.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(productListView, self).get_context_data(**kwargs)
        try:
            _, _, context['cartItems'] = getUserSpec(self.request)

        except (Exception, ):
            _, _, context['cartItems'] = getCartSpec(self.request)

        return context


def cart(request):
    if request.user.is_authenticated:
        items, order, cartItems = getUserSpec(request)
    else:
        items, order, cartItems = getCartSpec(request)

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    items, order, cartItems = getUserSpec(request)

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/checkout.html', context=context)


class productDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(productDetailView, self).get_context_data(**kwargs)
        try:
            _, _, context['cartItems'] = getUserSpec(self.request)

        except (Exception, ):
            _, _, context['cartItems'] = getCartSpec(self.request)

        return context


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = order.orderitem_set.get_or_create(product=product)

    if action == 'add':
        orderItem.quantity += 1

    elif action == 'reduce':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    if request.user.is_authenticated:
        makeTransaction(request)

    return JsonResponse('Order completed', safe=False)

