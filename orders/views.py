from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required # login required for functions
from django.contrib.auth.mixins import LoginRequiredMixin # login required for class based views
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic.detail import DetailView


import datetime
import stripe


from .models import Order , CartDetails , Cart , Coupon , OrderDetails , Wishlist
from products.models import Product
from settings.models import DeliveryFee
from utils.generate_code import generate_code
from userauths.models import Profile

def _update_cart_total_after_coupon(cart):
    """
    Recalculates the cart's total_after_coupon based on its current items
    and associated coupon. Clears coupon if invalid or expired.
    """
    coupon = cart.coupon
    cart_total_before_coupon = cart.cart_total() # Get current total

    if coupon:
        today_date = datetime.date.today()
        # Check if coupon is still valid (exists, quantity > 0, within date range)
        is_valid = (
            coupon.quantity > 0 and
            coupon.start_date <= today_date and
            (coupon.end_date is None or coupon.end_date >= today_date)
        )

        if is_valid:
            coupon_value = cart_total_before_coupon * coupon.discount / 100
            cart.total_after_coupon = round(cart_total_before_coupon - coupon_value, 2)
        else:
            # Coupon is invalid or expired, remove it and set total to cart total
            cart.coupon = None
            cart.total_after_coupon = round(cart_total_before_coupon, 2)
            # Optionally, add a message indicating coupon removal?
    else:
        # No coupon applied, set total to cart total
        cart.total_after_coupon = round(cart_total_before_coupon, 2)

    cart.save()
    return cart # Return the updated cart
# Create your views here.


class OrderListView(LoginRequiredMixin , ListView):
    model = Order
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset



def add_to_cart(request):
    quantity = request.POST['quantity']
    product = Product.objects.get(id=request.POST['product_id'])

    cart = Cart.objects.get(user = request.user, status='InProgress')
    cart_detail , creeate = CartDetails.objects.get_or_create(cart=cart, product=product)

    cart_detail.quantity = int(quantity)
    cart_detail.total = round(int(quantity) * product.price , 2)
    cart_detail.save()

    # Recalculate total after coupon if applicable
    _update_cart_total_after_coupon(cart)

    return redirect (f'/products/{product.slug}')


def remove_from_cart(request,id):
    cart_detail = CartDetails.objects.get(id=id)
    cart = cart_detail.cart # Get the cart before deleting the detail
    cart_detail.delete()
    # Recalculate total after coupon if applicable
    _update_cart_total_after_coupon(cart)
    return redirect('/products/')



def remove_from_checkout(request,id):
    cart_detail = CartDetails.objects.get(id=id)
    cart = cart_detail.cart # Get the cart before deleting the detail
    cart_detail.delete()
    # Recalculate total after coupon if applicable
    _update_cart_total_after_coupon(cart)
    return redirect('/orders/checkout')



@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user,status='InProgress')
    # Ensure cart total reflects current coupon status before proceeding
    cart = _update_cart_total_after_coupon(cart) # This now sets total_after_coupon correctly regardless
    cart_detail = CartDetails.objects.filter(cart=cart)
    delivery_fee_obj = DeliveryFee.objects.last()
    delivery_fee = delivery_fee_obj.fee if delivery_fee_obj else 0
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

    if request.method == 'POST':
        coupon = get_object_or_404(Coupon,code=request.POST['coupon_code']) # 404 with out coupon
        # coupon = Coupon.objects.get(code=request.data['coupon_code']) # erorr without coupon


        # Attempt to apply the coupon
        if coupon:
            original_coupon_on_cart = cart.coupon # Store original coupon state
            cart.coupon = coupon # Temporarily assign coupon to cart for validation
            cart = _update_cart_total_after_coupon(cart) # Validate and calculate

            # Check if the helper function actually applied THIS coupon (i.e., it was valid and different from original or original was None)
            coupon_was_applied = cart.coupon == coupon and cart.total_after_coupon != cart.cart_total()

            if coupon_was_applied:
                # Coupon was valid and applied, decrement quantity
                coupon.quantity -= 1
                coupon.save()
                coupon_value_display = cart.cart_total() - cart.total_after_coupon # Calculate discount amount
            else:
                # Coupon was invalid or didn't change the total (e.g., already applied)
                # The helper function already reset cart.coupon if invalid
                coupon_value_display = 0 # No discount applied in this attempt
                # Optionally add a message indicating the coupon was invalid/already applied?

            # Prepare values for response using the updated cart state from the helper
            cart_total_display = cart.total_after_coupon # Use the calculated total (discounted or not)
            total = delivery_fee + cart_total_display

            html = render_to_string('include/checkout_table.html',{
                'cart_detail': cart_detail,
                'sub_total': cart_total_display, # Updated sub_total
                'cart_total': total,
                'coupon': coupon_value_display, # Display the discount amount for this attempt
                'delivery_fee': delivery_fee,
                'pub_key':pub_key,
            })
            return JsonResponse({'result': html})

            # return render(request, 'orders/checkout.html',{
                #     'cart_detail': cart_detail,
                #     'sub_total': cart_total,
                #     'cart_total': total,
                #     'coupon': coupon_value,
                #     'delivery_fee': delivery_fee,
                # })
        else: # Coupon code not found in POST
             # No coupon code submitted, just re-render the table with current cart state
             cart = _update_cart_total_after_coupon(cart) # Ensure state is up-to-date
             cart_total_display = cart.total_after_coupon
             total = delivery_fee + cart_total_display
             coupon_value_display = cart.discount_amount() # Use model method for current discount

             html = render_to_string('include/checkout_table.html',{
                 'cart_detail': cart_detail,
                 'sub_total': cart_total_display,
                 'cart_total': total,
                 'coupon': coupon_value_display,
                 'delivery_fee': delivery_fee,
                 'pub_key':pub_key,
             })
             # Return error if coupon code was expected but not found? Depends on frontend logic.
             # For now, just return the current state.
             # return JsonResponse({'error': 'Coupon code not found.'}, status=404)


    # --- GET Request Logic ---
    else:
        # Helper was called at the start, so cart state is up-to-date
        sub_total = cart.total_after_coupon # This is now always the correct item total
        total = delivery_fee + sub_total
        coupon_value_display = cart.discount_amount() # Use the model method

    return render(request, 'orders/checkout.html',{
        'cart_detail': cart_detail,
        'sub_total': sub_total, # Display total after coupon if applied
        'cart_total': total,
        'coupon': coupon_value_display, # Display discount amount
        'delivery_fee': delivery_fee,
        'pub_key':pub_key,
    })




def process_payment(request):
    cart = Cart.objects.get(user=request.user, status='InProgress')

    if not cart:
        return JsonResponse({'error': 'No active cart found'}, status=400)

    cart_detail = CartDetails.objects.filter(cart=cart)
    delivery_fee_obj = DeliveryFee.objects.last()
    delivery_fee = delivery_fee_obj.fee if delivery_fee_obj else 0

    if cart.total_after_coupon:
        total = cart.total_after_coupon + delivery_fee
    else:
        total = cart.cart_total() + delivery_fee

    code = generate_code()

    stripe.api_key = settings.STRIPE_API_KEY_SECRET


    items = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': code,
                },
                'unit_amount': int(total * 100),
            },
            'quantity': 1,
        }
    ]

    checkout_session = stripe.checkout.Session.create(
        line_items=items,
        mode='payment',
        success_url="http://localhost:8004/orders/checkout/payment/success",  # استخدام HTTPS هنا
        cancel_url="http://localhost:8004/orders/checkout/payment/failed",  # استخدام HTTPS هنا
    )

    return JsonResponse({'session': checkout_session})



def payment_success(request):

    cart = Cart.objects.get(user=request.user, status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)

    new_order = Order.objects.create(
        user=request.user,
        coupon=cart.coupon,
        total_after_coupon=cart.total_after_coupon,
    )

    for item in cart_detail:
        OrderDetails.objects.create(
            order=new_order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            total=round(item.quantity * item.product.price, 2),
        )

    cart.status = 'Completed'
    cart.save()

    return render(request, 'orders/success.html')

@login_required
def update_cart_item_quantity(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity'))

            if quantity < 1: # Prevent zero or negative quantity
                 return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)

            cart_detail = get_object_or_404(CartDetails, id=item_id, cart__user=request.user, cart__status='InProgress')
            product = cart_detail.product

            # Update item details
            cart_detail.quantity = quantity
            cart_detail.total = round(quantity * product.price, 2)
            cart_detail.save()

            # Update main cart totals
            cart = cart_detail.cart
            cart = _update_cart_total_after_coupon(cart) # Recalculate total after coupon

            # Prepare data for response
            cart_detail_data = CartDetails.objects.filter(cart=cart)
            item_count = cart_detail_data.count()
            cart_total_val = cart.total_after_coupon # This now holds the correct total (with or without coupon)

            # Consider delivery fee if needed for display (though usually added at checkout)
            # delivery_fee_obj = DeliveryFee.objects.last()
            # delivery_fee = delivery_fee_obj.fee if delivery_fee_obj else 0
            # display_total = cart_total_val + delivery_fee

            return JsonResponse({
                'success': True,
                'item_id': item_id,
                'new_item_total': cart_detail.total,
                'new_cart_subtotal': cart_total_val, # Renamed for clarity (it's the item total after potential coupon)
                'new_item_count': item_count,
                'discount_amount': cart.discount_amount(), # Send discount amount
            })

        except CartDetails.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Product.DoesNotExist:
             return JsonResponse({'error': 'Product associated with cart item not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
        except Exception as e:
            # Log the exception e
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def payment_failed(request):
    return render(request,'orders/failed.html')


def coupon(request):
    coupon = Coupon.objects.all()
    context={
        'coupon': coupon,
    }
    return render(request,'orders/coupon.html',context)



def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        context = {
            'wishlist_items': wishlist_items,
        }
        return render(request, 'orders/wishlist.html', context)
    else:
        return redirect('userauths:sign-in')



def remove_from_wishlist(request, pk):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wishlist_item.delete()
        return redirect('orders:wishlist')
    return redirect('userauths:sign-in')



@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wishlist_item.delete()
    
    return redirect('orders:wishlist')
