import json
import datetime
from .models import Product, Order, ShippingAddress, OrderItem


def getCartSpec(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except (Exception,):
        cart = {}

    items = []
    order = {'get_order_total_price': 0, 'get_order_total_items': 0}
    cartItems = 0

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_order_total_price'] += total
            order['get_order_total_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': i,
                    'title': product.title,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity': cart[i]['quantity'],
                'get_total_price': total,
            }

            items.append(item)

        except (Exception,):
            continue

    return items, order, cartItems


def getUserSpec(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    cartItems = order.get_order_total_items

    return items, order, cartItems


def mergeItems(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    cookieItems, _, _ = getCartSpec(request)

    for cookieItem in cookieItems:
        for item in items:
            if int(item.product.id) == int(cookieItem['product']['id']):
                item.quantity += cookieItem['quantity']
                item.save()
                break
        else:
            product = Product.objects.get(id=cookieItem['product']['id'])
            OrderItem.objects.create(product=product, order=order, quantity=cookieItem['quantity'])


def makeTransaction(request):
    transaction = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    address = data['shipping']['address']
    city = data['shipping']['city']
    country = data['shipping']['country']

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.transaction = transaction

    order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        city=city,
        country=country,
        address=address,
    )
