from django.urls import path
from .views import (
    home, permission_denied_view, users_list_view, user_create_view, user_update_view, user_delete_view, # Added user_delete_view
    profiles_list_view, # Added profile_update_view
    addresses_list_view, address_create_view, # Added address_create_view
    phones_list_view, phone_create_view, # Added phone_create_view
    credit_cards_list_view, credit_card_create_view, # Added credit_card_create_view
    products_list_view, brands_list_view, brand_create_view, brand_update_view, brand_delete_view, reviews_list_view, # Added brand update/delete
    product_create_view, product_update_view, product_delete_view,
    orders_list_view, order_create_view, order_update_view, order_delete_view, # Added order views
    carts_list_view, # Added cart list view
    get_product_price_api, review_delete_view,
    coupons_list_view, coupon_create_view, coupon_update_view, coupon_delete_view, # Added coupon CRUD views
    wishlists_list_view, # Added wishlist list view
    company_details_view, delivery_fee_view # Added settings views
)
# Import product CRUD views from the products app
#from products.views import product_create_view, product_update_view, product_delete_view

app_name = 'administration'

urlpatterns = [
    path('', home, name='home'),
    path('error/', permission_denied_view, name='error_page'),
    path('users/', users_list_view, name='users_list'),
    path('users/create/', user_create_view, name='user_create'), # Added user create URL
    path('users/<int:user_id>/update/', user_update_view, name='user_update'), # Added user update URL
    path('users/<int:user_id>/delete/', user_delete_view, name='user_delete'), # Added user delete URL
    path('profiles/', profiles_list_view, name='profiles_list'),
    #path('profiles/<int:profile_id>/update/', profile_update_view, name='profile_update'), # Added profile update URL
    path('addresses/', addresses_list_view, name='addresses_list'),
    path('addresses/create/', address_create_view, name='address_create'), # Added address create URL
    path('phones/', phones_list_view, name='phones_list'),
    path('phones/create/', phone_create_view, name='phone_create'), # Added phone create URL
    path('credit-cards/', credit_cards_list_view, name='credit_cards_list'), # Added URL for credit cards list
    path('credit-cards/create/', credit_card_create_view, name='credit_card_create'), # Added credit card create URL
    path('products/', products_list_view, name='products_list'),
    # Add Product CRUD URLs under administration
    path('products/create/', product_create_view, name='product_create'),
    path('products/<slug:slug>/update/', product_update_view, name='product_update'),
    path('products/<slug:slug>/delete/', product_delete_view, name='product_delete'),

    path('brands/', brands_list_view, name='brands_list'),
    # API URL for fetching product price
    path('api/product-price/<int:product_id>/', get_product_price_api, name='api_get_product_price'),
    path('brands/create/', brand_create_view, name='brand_create'), # Added URL for brand creation
    path('brands/<int:pk>/update/', brand_update_view, name='brand_update'), # Added URL for brand update
    path('brands/<int:pk>/delete/', brand_delete_view, name='brand_delete'), # Added URL for brand delete
    path('reviews/', reviews_list_view, name='reviews_list'),
    path('reviews/<int:pk>/delete/', review_delete_view, name='review_delete'),

    # Order URLs
    path('orders/', orders_list_view, name='orders_list'),
    path('orders/create/', order_create_view, name='order_create'), # Added order create URL
    path('orders/<int:pk>/update/', order_update_view, name='order_update'),
# Cart URLs
    path('carts/', carts_list_view, name='carts_list'),
    path('orders/<int:pk>/delete/', order_delete_view, name='order_delete'),

    # Coupon URLs
    path('coupons/', coupons_list_view, name='coupons_list'),
    path('coupons/create/', coupon_create_view, name='coupon_create'), # Added coupon create URL
    path('coupons/<int:pk>/update/', coupon_update_view, name='coupon_update'), # Added coupon update URL
    path('coupons/<int:pk>/delete/', coupon_delete_view, name='coupon_delete'), # Added coupon delete URL

    # Wishlist URLs
    path('wishlists/', wishlists_list_view, name='wishlists_list'),

    # Settings URLs
    path('settings/company/', company_details_view, name='company_details'),
    path('settings/delivery-fee/', delivery_fee_view, name='delivery_fee'),
]