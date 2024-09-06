""" payment views """
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart

from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingForm, PaymentForm
from users.models import Profile


@login_required
def orders(request, pk):
    if request.user.is_authenticated:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # check if true or false
            if status == 'true':
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = timezone.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('books')
        
        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.warning(request, "Access Denied")
        return redirect('books')

@login_required
def not_shipped_dash(request):
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            # grab Date and time
            now = timezone.now()
            # grab the order
            order = Order.objects.filter(id=num)
            # update order
            order.update(shipped=True, date_shipped=now)
            
            messages.success(request, "Shipping status updated")
            return redirect('books')
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.warning(request, "Access Denied")
        return redirect('books')

@login_required
def shipped_dash(request):
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            # grab Data time
            now = timezone.now()
            # grab the order
            order = Order.objects.filter(id=num)
            order.update(shipped=False)

            messages.success(request, "Shipping status updated")
            return redirect('books')
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.warning(request, "Access Denied")
        return redirect('books')

def process_order(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_books = cart.get_books
        quantities = cart.get_quantities
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"""{my_shipping['shipping_address1']}
        \n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}
        \n{my_shipping['shipping_state']}
        \n{my_shipping['shipping_zipcode']}
        \n{my_shipping['shipping_country']}"""
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_oder = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_oder.save()

            # Add order items
            # Get the order ID
            order_id = create_oder.pk

            # Get book Info
            for book in cart_books():
                # Get book ID
                book_id = book.id
                # Get book price
                if book.is_sale:
                    price = book.sale_price
                else:
                    price = book.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == book.id:
                        # create order item
                        create_oder_item = OrderItem(order_id=order_id, book_id=book_id, user=user, quantity=value, price=price)
                        create_oder_item.save()
                
            # Delete our cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (user_cart field)
            currente_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in Database (user_cart field)
            currente_user.update(user_cart="")
            
            messages.success(request, "Order Placed!")
            return redirect('books')
        else:
            # Not looged in
            # Create Order
            create_oder = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_oder.save()
            # Add order items
            # Get the order ID
            order_id = create_oder.pk

            # Get book Info
            for book in cart_books():
                # Get book ID
                book_id = book.id
                # Get book price
                if book.is_sale:
                    price = book.sale_price
                else:
                    price = book.price

                # Get quantity
                for key, value in quantities().item():
                    if int(key) == book.id:
                        # create order item
                        create_oder_item = OrderItem(order_id=order_id, book_id=book_id, quantity=value, price=price)
                        create_oder_item.save()
                        
            # Delete our cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    # Delete the key
                    del request.session[key]
            messages.success(request, 'Order Placed!')
            return redirect('books')
    else:
        messages.warning(request, 'Access Denied')
        return redirect('books')

def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_books = cart.get_books
        quantities = cart.get_quantities
        totals = cart.cart_total()

        # create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {
                'cart_books': cart_books,
                'quantities': quantities,
                'totals': totals,
                'shipping_info': request.POST,
                'billing_form': billing_form
            })
        else:
            # Not logged in
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {
                'cart_books': cart_books,
                'quantities': quantities,
                'totals': totals,
                'shipping_info': request.POST,
                'billing_form': billing_form
            })
    else:
        messages.warning(request, 'Access Denied')
        return redirect('books')

def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quantities
    totals = cart.cart_total()

    if request.user.i_authenticated:
        # Checkout as logged in user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {
            'cart_books': cart_books,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        })
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {
            'cart_books': cart_books,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        })
    
def payment_success(request):
    return render(request, 'payment/payment_success.html')