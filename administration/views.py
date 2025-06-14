from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from userauths.models import User, Profile, Address, Phone, CreditCard # Added CreditCard import
from settings.models import Company, DeliveryFee # Import DeliveryFee as well
from products.models import Product, ProductImage, Brand, Review
from orders.models import Order, Cart, Coupon, Wishlist # Import Order, Cart, Coupon, Wishlist models
from .forms import ProductForm, OrderForm, OrderCreateForm, OrderDetailCreateInlineFormSet, OrderDetailUpdateInlineFormSet, CompanyForm, DeliveryFeeForm # Import CompanyForm and DeliveryFeeForm
# Create your views here.
from django.db import transaction # Import transaction
from django.contrib.auth.decorators import login_required, user_passes_test # Import decorators
from django.contrib import messages # Add messages import
from userauths.forms import ProfileForm, UpdateProfileForm # Import ProfileForm
from django.contrib.auth.forms import UserChangeForm # Keep UserChangeForm - wait, no, remove this if not used elsewhere
from .forms import AdminSetPasswordForm, AdminUserCreationForm, AdminUserChangeForm, AddressForm, PhoneForm, CreditCardForm, BrandForm, CouponForm # Import AddressForm, PhoneForm, CreditCardForm, BrandForm, CouponForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator


def test(request):
    return HttpResponse('great')

# Helper function to check if user is staff (adjust as needed)
def is_staff_user(user):
    return user.is_staff


@login_required(login_url="/login")
def home(request):
    # Check if user is authenticated
    # if not request.user.is_authenticated:
    #     # Redirect to login page if not logged in
    #     return redirect('userauths:sign-in') # Please confirm or provide the correct login URL name

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        # Redirect non-admin users to an error page
        return redirect('administration:error_page') # Please confirm or provide the correct error page URL name

    user = request.user
    company = get_company_data()
    return render(request, 'administration/homie.html', {'user': user, 'company':company})

def permission_denied_view(request):
    """
    View to render the permission denied error page.
    """
    return render(request, 'administration/error_page.html', status=403)

def get_company_data():
    data = Company.objects.last()
    # fee = DeliveryFee.objects.last()
    return data

# View for Profiles List
def profiles_list_view(request):
    """
    View to display a list of all user profiles.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    profiles = Profile.objects.all().select_related('user', 'address', 'phone') # Optimize query
    context = {
        'profiles': profiles,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/profiles_list.html', context)


# View for Addresses List
def addresses_list_view(request):
    """
    View to display a list of all addresses.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    addresses = Address.objects.all().select_related('user') # Optimize query
    context = {
        'addresses': addresses,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/addresses_list.html', context)


# View for Phones List
def phones_list_view(request):
    """
    View to display a list of all phone numbers.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    phones = Phone.objects.all().select_related('user') # Optimize query
    context = {
        'phones': phones,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/phones_list.html', context)


# View for Credit Cards List
def credit_cards_list_view(request):
    """
    View to display a list of all credit cards.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    credit_cards = CreditCard.objects.all().select_related('user') # Optimize query
    context = {
        'credit_cards': credit_cards,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/credit_cards_list.html', context)

# View for Creating an Address
@login_required
@user_passes_test(is_staff_user)
def address_create_view(request):
    """
    View to handle the creation of a new address.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to create addresses.")
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            # Removed is_default handling as it's not in the model
            messages.success(request, f'Address for user {address.user.username} created successfully!')
            return redirect('administration:addresses_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddressForm()

    context = {
        'form': form,
        'form_title': 'Create New Address',
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a template named 'address_form.html'
    return render(request, 'administration/address_form.html', context)


# View for Creating a Phone
@login_required
@user_passes_test(is_staff_user)
def phone_create_view(request):
    """
    View to handle the creation of a new phone number.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to create phone numbers.")
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.save()
             # Removed is_default handling as it's not in the model
            messages.success(request, f'Phone number for user {phone.user.username} created successfully!')
            return redirect('administration:phones_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PhoneForm()

    context = {
        'form': form,
        'form_title': 'Create New Phone Number',
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a template named 'phone_form.html'
    return render(request, 'administration/phone_form.html', context)
# View for Creating a Credit Card
@login_required
@user_passes_test(is_staff_user)
def credit_card_create_view(request):
    """
    View to handle the creation of a new credit card.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to create credit cards.")
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = CreditCardForm(request.POST, request.FILES) # Include request.FILES for image upload
        if form.is_valid():
            credit_card = form.save()
            messages.success(request, f'Credit card ending in {credit_card.card_number[-4:]} for user {credit_card.user.username} created successfully!')
            return redirect('administration:credit_cards_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CreditCardForm()

    context = {
        'form': form,
        'form_title': 'Create New Credit Card',
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a template named 'credit_card_form.html'
    return render(request, 'administration/credit_card_form.html', context)

# View for Users List
def users_list_view(request):
    """
    View to display a list of all users.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page') # Use the namespaced URL

    users = User.objects.all()
    context = {
        'users': users,
        'user': request.user, # Pass user for base template context if needed
        'company': get_company_data() # Pass company data if needed by base template
    }
    return render(request, 'administration/users_list.html', context)

# View for Products List
def products_list_view(request):
    """
    View to display a list of all products.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    products = Product.objects.all().select_related('brand').prefetch_related('product_image') # Optimize query with prefetch
    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'products': page_obj,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/products_list.html', context)


# View for Brands List
def brands_list_view(request):
    """
    View to display a list of all brands.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    brands = Brand.objects.all()
    context = {
        'brands': brands,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/brands_list.html', context)

# View for Reviews List
def reviews_list_view(request):
    """
    View to display a list of all reviews.
    Requires authentication and superuser status.
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:sign-in')

    # Check if the authenticated user is a superuser
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    reviews = Review.objects.all().select_related('user', 'product') # Optimize query
    context = {
        'reviews': reviews,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/reviews_list.html', context)



from .forms import BrandForm # Import the Brand form



# View for Creating a Brand
@login_required
@user_passes_test(is_staff_user) # Assuming is_staff_user helper exists or add it
def brand_create_view(request):
    """
    View to handle the creation of a new brand.
    Requires authentication and superuser status.
    """
    # Basic permission check (adjust as needed)
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand created successfully!')
            return redirect('administration:brands_list') # Redirect to the list view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BrandForm()

    context = {
        'form': form,
        'form_title': 'Create New Brand', # Title for the template
        'user': request.user,
        'company': get_company_data() # Assuming get_company_data exists
    }
    # Ensure this template exists
    return render(request, 'administration/brand_form.html', context)

# View for Updating a Brand
@login_required
@user_passes_test(is_staff_user)
def brand_update_view(request, pk):
    """
    View to handle updating an existing brand.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to update brands.")
        return redirect('administration:error_page')

    brand_to_update = get_object_or_404(Brand, pk=pk)

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f'Brand "{brand_to_update.name}" updated successfully!')
            return redirect('administration:brands_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BrandForm(instance=brand_to_update)

    context = {
        'form': form,
        'form_title': f'Update Brand: {brand_to_update.name}',
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/brand_form.html', context)


# View for Deleting a Brand
@login_required
@user_passes_test(is_staff_user)
def brand_delete_view(request, pk):
    """
    View to handle deleting an existing brand.
    Requires authentication and superuser status.
    Displays a confirmation page before deletion.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete brands.")
        return redirect('administration:error_page')

    brand_to_delete = get_object_or_404(Brand, pk=pk)

    if request.method == 'POST':
        brand_name = brand_to_delete.name # Store name for message
        brand_to_delete.delete()
        messages.success(request, f"Brand '{brand_name}' deleted successfully.")
        return redirect('administration:brands_list')

    context = {
        'object_to_delete': brand_to_delete,
        'object_type': 'Brand',
        'cancel_url': reverse_lazy('administration:brands_list'),
        'form_title': f'Confirm Delete Brand: {brand_to_delete.name}',
        'user': request.user,
        'company': get_company_data()
    }
    # Reuse the generic confirm_delete template
    return render(request, 'administration/confirm_delete.html', context)
# View for Creating a User
@login_required
@user_passes_test(is_staff_user) # Ensure only staff can access
def user_create_view(request):
    """
    View to handle the creation of a new user.
    Requires authentication and staff status.
    """
    if not request.user.is_superuser: # Or a more specific permission check
        messages.error(request, "You do not have permission to create users.")
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST) # Use the custom admin form
        if form.is_valid():
            new_user = form.save() # Save the user and get the instance
            # Profile is created automatically by a signal in userauths/models.py
            messages.success(request, f'User {new_user.username} created successfully!') # Reverted message
            return redirect('administration:users_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserCreationForm() # Use the custom admin form

    context = {
        'form': form,
        'form_title': 'Create New User',
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/user_form.html', context)

# View for Updating a User
@login_required
@user_passes_test(is_staff_user) # Ensure only staff can access
def user_update_view(request, user_id):
    """
    View to handle updating an existing user.
    Requires authentication and staff status.
    """
    if not request.user.is_superuser: # Or a more specific permission check
        messages.error(request, "You do not have permission to update users.")
        return redirect('administration:error_page')

    user_to_update = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Use AdminUserChangeForm for updates
        form = AdminUserChangeForm(request.POST, instance=user_to_update) # Use custom form
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_to_update.username} updated successfully!')
            return redirect('administration:users_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserChangeForm(instance=user_to_update) # Use custom form

    context = {
        'form': form,
        'form_title': f'Update User: {user_to_update.username}',
        'user': request.user,
        'company': get_company_data()
    } # Add missing closing brace
    return render(request, 'administration/user_form.html', context) # Add missing return statement



@login_required
@user_passes_test(is_staff_user)
def user_change_password_view(request, user_id):
    """
    View to handle changing password for an existing user.
    Requires authentication and staff status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to change user passwords.")
        return redirect('administration:error_page')

    user_to_update = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminSetPasswordForm(user_to_update, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Password for {user_to_update.username} changed successfully!')
            return redirect('administration:users_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminSetPasswordForm(user_to_update)

    context = {
        'form': form,
        'form_title': f'Change Password for: {user_to_update.username}',
        'user_to_update': user_to_update,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/password_change_form.html', context)


# View for Deleting a User
@login_required
@user_passes_test(is_staff_user) # Ensure only staff can access
def user_delete_view(request, user_id):
    """
    View to handle deleting an existing user.
    Requires authentication and staff status.
    Displays a confirmation page before deletion.
    """
    if not request.user.is_superuser: # Or a more specific permission check
        messages.error(request, "You do not have permission to delete users.")
        return redirect('administration:error_page')

    user_to_delete = get_object_or_404(User, id=user_id)

    # Prevent users from deleting themselves
    if request.user == user_to_delete:
        messages.error(request, "You cannot delete your own account.")
        return redirect('administration:users_list')

    if request.method == 'POST':
        user_username = user_to_delete.username # Store username for message
        user_to_delete.delete()
        messages.success(request, f"User '{user_username}' deleted successfully.")
        return redirect('administration:users_list')

    context = {
        'object_to_delete': user_to_delete, # Use a generic name for template reusability
        'object_type': 'User',
        'cancel_url': reverse_lazy('administration:users_list'), # URL to go back to
        'form_title': f'Confirm Delete User: {user_to_delete.username}',
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a confirmation template, e.g., 'confirm_delete.html'
    # Let's assume a generic one exists for now or create one next.
    # Reusing product_confirm_delete for now, but ideally create user_confirm_delete.html
    return render(request, 'administration/confirm_delete.html', context)



# View for Deleting a profile
@login_required
@user_passes_test(is_staff_user) # Ensure only staff can access
def profile_delete_view(request, profile_id):
    """
    View to handle deleting an existing user.
    Requires authentication and staff status.
    Displays a confirmation page before deletion.
    """
    if not request.user.is_superuser: # Or a more specific permission check
        messages.error(request, "You do not have permission to delete users.")
        return redirect('administration:error_page')
    
    profile_to_delete = get_object_or_404(Profile, id=profile_id)

    user_to_delete = profile_to_delete.user

    # Prevent users from deleting themselves
    if request.user == user_to_delete:
        messages.error(request, "You cannot delete your own account.")
        return redirect('administration:users_list')

    if request.method == 'POST':
        user_username = user_to_delete.username # Store username for message
        profile_to_delete.delete()
        user_to_delete.delete()
        messages.success(request, f"Profile '{user_username}' deleted successfully.")
        return redirect('administration:profiles_list')

    context = {
        'object_to_delete': user_to_delete, # Use a generic name for template reusability
        'object_type': 'Profile',
        'cancel_url': reverse_lazy('administration:profiles_list'), # URL to go back to
        'form_title': f'Confirm Delete Profile: {user_to_delete.username}',
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a confirmation template, e.g., 'confirm_delete.html'
    # Let's assume a generic one exists for now or create one next.
    # Reusing product_confirm_delete for now, but ideally create user_confirm_delete.html
    return render(request, 'administration/confirm_delete.html', context)

# Remove duplicated closing brace and return statement from the previous fix

# View for Updating a Profile
@login_required
@user_passes_test(is_staff_user)  # Ensure only staff can access
def profile_update_view(request, profile_id):
    """
    View to handle updating an existing user profile.
    Requires authentication and staff status.
    """
    if not request.user.is_superuser:  # Or a more specific permission check
        messages.error(request, "You do not have permission to update profiles.")
        return redirect('administration:error_page')

    profile_to_update = get_object_or_404(Profile, id=profile_id)
    user_to_update = profile_to_update.user  # Get the associated user
    
    # Get the user's primary address and phone (if applicable)
    try:
        primary_address = Address.objects.filter(user=user_to_update).first()
        primary_phone = Phone.objects.filter(user=user_to_update).first()
    except:
        primary_address = None
        primary_phone = None

    if request.method == 'POST':
        form = UpdateProfileForm(
            request.POST, 
            request.FILES, 
            instance=profile_to_update,
            user=user_to_update  # Pass the user parameter required by the form
        )
        if form.is_valid():
            profile = form.save()
            
            # Update selected address and phone relationships if needed
            selected_address = form.cleaned_data.get('address')
            selected_phone = form.cleaned_data.get('phone')
            
            # Here you could mark the selected address/phone as primary
            # This depends on your data model - adjust as needed
            
            messages.success(request, f'Profile for {user_to_update.username} updated successfully!')
            return redirect('administration:profiles_list')  # Redirect back to profiles list
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Set initial data for the address and phone fields
        initial_data = {}
        if primary_address:
            initial_data['address'] = primary_address.id
        if primary_phone:
            initial_data['phone'] = primary_phone.id
            
        form = UpdateProfileForm(
            instance=profile_to_update,
            user=user_to_update,  # Pass the user parameter required by the form
            initial=initial_data  # Set initial values for our select fields
        )

    context = {
        'form': form,
        'form_title': f'Update Profile: {user_to_update.username}',
        'user': request.user,
        'company': get_company_data(),
        'addresses': Address.objects.filter(user=user_to_update),
        'phones': Phone.objects.filter(user=user_to_update),
    }
    
    return render(request, 'administration/profile_form.html', context)

@login_required
@user_passes_test(is_staff_user)
@transaction.atomic # Ensure atomicity for product and images saving
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # Use 'form' variable name
        if form.is_valid():
            product = form.save()

            # Handle multiple image uploads
            new_images = form.cleaned_data.get('new_images', [])
            for image_file in new_images:
                if image_file: # Check if file is valid
                    ProductImage.objects.create(product=product, image=image_file)

            messages.success(request, f"Product '{product.name}' created successfully.")
            # Redirect to the product list within the administration app
            return redirect('administration:products_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm() # Use 'form' variable name

    context = {
        'form': form, # Use 'form' as the key
        'form_title': 'Create New Product',
        # Add other necessary context if templates/base.html requires it
        # 'user': request.user,
        # 'company': get_company_data() # Need to define or import get_company_data if used
    }
    # Use template within products app
    return render(request, 'administration/products_form.html', context)

@login_required
@user_passes_test(is_staff_user)
@transaction.atomic
def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product) # Use 'form' variable name
        if form.is_valid():
            form.save() # Save product details first

            # Handle multiple new image uploads
            new_images = form.cleaned_data.get('new_images', [])
            for image_file in new_images:
                 if image_file: # Check if file is valid
                    ProductImage.objects.create(product=product, image=image_file)

            # Handle deletion of existing images
            for key in request.POST:
                if key.startswith('delete_image_'):
                    try:
                        image_id = int(key.split('_')[-1])
                        image_to_delete = ProductImage.objects.get(id=image_id, product=product)
                        image_to_delete.delete()
                        # Optionally delete the file from storage here too
                    except (ValueError, ProductImage.DoesNotExist):
                        messages.warning(request, f"Could not delete image with ID {key.split('_')[-1]}.")


            messages.success(request, f"Product '{product.name}' updated successfully.")
            # Redirect to the product list within the administration app
            return redirect('administration:products_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product) # Use 'form' variable name

    context = {
        'form': form, # Use 'form' as the key
        'product': product,
        'form_title': f'Update Product: {product.name}',
        # Add other necessary context if templates/base.html requires it
        # 'user': request.user,
        # 'company': get_company_data() # Need to define or import get_company_data if used
    }
     # Use template within products app
    return render(request, 'administration/products_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def product_delete_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully.")
        # Redirect to the product list within the products app OR administration list?
        # Let's assume products list for now, adjust if needed.
        return redirect('administration:products_list')

    context = {
        'product': product,
        # Add other necessary context if templates/base.html requires it
        # 'user': request.user,
        # 'company': get_company_data() # Need to define or import get_company_data if used
    }
    # Use template within products app
    return render(request, 'administration/product_confirm_delete.html', context)

# === Order Management Views ===

# View for Carts List
@login_required
@user_passes_test(is_staff_user) # Ensure only staff can access
def carts_list_view(request):
    """
    View to display a list of all shopping carts.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to view carts.")
        return redirect('administration:error_page')

    # Fetch carts, optimize with related user/coupon and prefetch details/products
    carts = Cart.objects.all().select_related(
        'user', 'coupon'
    ).prefetch_related(
        'cart_details', 'cart_details__product'
    ).order_by('-id') # Order by ID or another relevant field

    context = {
        'carts': carts,
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a template named 'carts_list.html'
    return render(request, 'administration/carts_list.html', context)
@login_required
@user_passes_test(is_staff_user)
def orders_list_view(request):
    """
    View to display a list of all orders.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    orders = Order.objects.all().select_related('user').order_by('-order_time') # Optimize and order by correct field
    context = {
        'orders': orders,
        'user': request.user,
        'company': get_company_data()
    }
    # We'll need a template named 'orders_list.html'
    return render(request, 'administration/orders_list.html', context)
@login_required
@user_passes_test(is_staff_user)
def order_create_view(request):
    """
    View to handle the creation of a new order, including its details (products).
    Requires authentication and superuser status.
    Uses an inline formset for OrderDetails.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to create orders.")
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        # Instantiate formset with POST data, but no instance yet
        formset = OrderDetailCreateInlineFormSet(request.POST, prefix='details') # Use Create formset

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic(): # Use transaction for atomicity
                    # Save the main order first to get a PK
                    order = form.save()

                    # Now save the formset, linking it to the created order instance
                    formset.instance = order
                    formset.save()

                    # --- Calculate and save the total AFTER details are saved ---
                    # Refresh order instance to ensure details are loaded if needed,
                    # though accessing order.order_details should work directly.
                    # order.refresh_from_db() # Optional, but can be good practice

                    raw_total = sum(detail.total for detail in order.order_details.all() if detail.total is not None)
                    if order.coupon:
                        discount_amount = raw_total * (order.coupon.discount / 100.0)
                        order.total_after_coupon = round(raw_total - discount_amount, 2)
                    else:
                        order.total_after_coupon = round(raw_total, 2)
                    order.save(update_fields=['total_after_coupon']) # Save only the updated field
                    # --- End total calculation ---

                    messages.success(request, f'Order #{order.pk} created successfully with total calculated!')
                    return redirect('administration:orders_list') # Redirect to list view after successful creation
            except Exception as e:
                 # Catch potential errors during save
                 messages.error(request, f"An error occurred while saving the order: {e}")

        else:
            # Combine form and formset errors for display
            error_message = "Please correct the errors below."
            if form.errors:
                error_message += " (Order details)"
            if formset.errors or formset.non_form_errors():
                 error_message += " (Product items)"
            messages.error(request, error_message)
            # Fall through to render the form and formset with errors below

    else: # GET request
        form = OrderCreateForm()
        # Instantiate an empty formset for the template, with extra forms for creation
        formset = OrderDetailCreateInlineFormSet(prefix='details') # Use Create formset

    context = {
        'form': form,
        'formset': formset, # Add formset to context
        'form_title': 'Create New Order',
        'user': request.user,
        'company': get_company_data()
    }
    # Reuse the order_form template
    return render(request, 'administration/order_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def order_update_view(request, pk):
    """
    View to handle updating an existing order (status) and its details (products).
    Requires authentication and superuser status.
    Uses OrderForm for status and OrderDetailInlineFormSet for items.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to update orders.")
        return redirect('administration:error_page')

    order_to_update = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_to_update)
        # Instantiate formset with POST data and the order instance
        # Override defaults to make it read-only for update view
        # Use Update formset (extra=0, can_delete=False are defined in the formset class itself)
        formset = OrderDetailUpdateInlineFormSet(
            request.POST,
            instance=order_to_update,
            prefix='details'
        )

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the main order form (status)
                    form.save()
                    # Save the inline formset (order details)
                    formset.save()

                    # --- Recalculate and save the total AFTER details are updated ---
                    # The order_to_update instance should reflect the latest details now.
                    raw_total = sum(detail.total for detail in order_to_update.order_details.all() if detail.total is not None)
                    if order_to_update.coupon:
                        discount_amount = raw_total * (order_to_update.coupon.discount / 100.0)
                        order_to_update.total_after_coupon = round(raw_total - discount_amount, 2)
                    else:
                        order_to_update.total_after_coupon = round(raw_total, 2)
                    order_to_update.save(update_fields=['total_after_coupon']) # Save only the updated field
                    # --- End total recalculation ---

                    messages.success(request, f'Order #{order_to_update.pk} updated successfully and total recalculated!')
                    return redirect('administration:orders_list')
            except Exception as e:
                messages.error(request, f"An error occurred while saving the order: {e}")
        else:
            # Combine form and formset errors for display
            error_message = "Please correct the errors below."
            if form.errors:
                error_message += " (Order status)"
            if formset.errors or formset.non_form_errors():
                 error_message += " (Product items)"
            messages.error(request, error_message)
            # Fall through to render the form and formset with errors below

    else: # GET request
        form = OrderForm(instance=order_to_update)
        # Instantiate formset with the order instance for display
        formset = OrderDetailUpdateInlineFormSet(instance=order_to_update, prefix='details') # Use Update formset

    context = {
        'form': form,
        'formset': formset, # Add formset to context
        # 'order': order_to_update, # No longer needed, form.instance has the order
        'form_title': f'Update Order #{order_to_update.pk}', # Dynamic title
        'user': request.user,
        'company': get_company_data()
    }
    # Reuse the order_form template
    return render(request, 'administration/order_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def order_delete_view(request, pk):
    """
    View to handle deleting an existing order.
    Requires authentication and superuser status.
    Displays a confirmation page before deletion.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete orders.")
        return redirect('administration:error_page')

    order_to_delete = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order_pk = order_to_delete.pk # Store pk for message
        order_to_delete.delete()
        messages.success(request, f"Order #{order_pk} deleted successfully.")
        return redirect('administration:orders_list')

    context = {
        'object_to_delete': order_to_delete,
        'object_type': 'Order',
        'object_identifier': f"#{order_to_delete.pk}", # Specific identifier for orders
        'cancel_url': reverse_lazy('administration:orders_list'),
        'form_title': f'Confirm Delete Order #{order_to_delete.pk}',
        'user': request.user,
        'company': get_company_data()
    }
    # Reuse the generic confirm_delete template
    return render(request, 'administration/confirm_delete.html', context)

# API View for Product Price
@login_required
@user_passes_test(is_staff_user)
def get_product_price_api(request, product_id):
    """
    API endpoint to fetch the price of a product.
    Returns JSON response: {'price': product.price} or {'error': 'Product not found'}
    """
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({'price': product.price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        # Log the error e for debugging
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


@login_required
@user_passes_test(is_staff_user)
def review_delete_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete orders.")
        return redirect('administration:error_page')

    review_to_delete = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review_pk = review_to_delete.pk # Store pk for message
        review_to_delete.delete()
        messages.success(request, f"Review #{review_pk} deleted successfully.")
        return redirect('administration:reviews_list')

    context = {
        'object_to_delete': review_to_delete,
        'object_type': 'Review',
        'object_identifier': f"#{review_to_delete.pk}", # Specific identifier for orders
        'cancel_url': reverse_lazy('administration:reviews_list'),
        'form_title': f'Confirm Delete Review #{review_to_delete.pk}',
        'user': request.user,
        'company': get_company_data()
    }
    # Reuse the generic confirm_delete template
    return render(request, 'administration/confirm_delete.html', context)


# View for Coupons List
@login_required
@user_passes_test(is_staff_user)
def coupons_list_view(request):
    """
    View to display a list of all coupons.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/coupons_list.html', context)


# View for Creating a Coupon
@login_required
@user_passes_test(is_staff_user)
def coupon_create_view(request):
    """
    View to handle the creation of a new coupon.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to create coupons.")
        return redirect('administration:error_page')

    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon created successfully!')
            return redirect('administration:coupons_list') # Redirect to the list view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CouponForm()

    context = {
        'form': form,
        'form_title': 'Create New Coupon', # Title for the template
        'user': request.user,
        'company': get_company_data()
    }
    # Ensure this template exists
    return render(request, 'administration/coupon_form.html', context)
# View for Updating a Coupon
@login_required
@user_passes_test(is_staff_user)
def coupon_update_view(request, pk):
    """
    View to handle updating an existing coupon.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to update coupons.")
        return redirect('administration:error_page')

    coupon_to_update = get_object_or_404(Coupon, pk=pk)

    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES, instance=coupon_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f'Coupon "{coupon_to_update.code}" updated successfully!')
            return redirect('administration:coupons_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CouponForm(instance=coupon_to_update)

    context = {
        'form': form,
        'form_title': f'Update Coupon: {coupon_to_update.code}',
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/coupon_form.html', context)


# View for Deleting a Coupon
@login_required
@user_passes_test(is_staff_user)
def coupon_delete_view(request, pk):
    """
    View to handle deleting an existing coupon.
    Requires authentication and superuser status.
    Displays a confirmation page before deletion.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete coupons.")
        return redirect('administration:error_page')

    coupon_to_delete = get_object_or_404(Coupon, pk=pk)

    if request.method == 'POST':
        coupon_code = coupon_to_delete.code # Store code for message
        coupon_to_delete.delete()
        messages.success(request, f"Coupon '{coupon_code}' deleted successfully.")
        return redirect('administration:coupons_list')

    context = {
        'object_to_delete': coupon_to_delete,
        'object_type': 'Coupon',
        'cancel_url': reverse_lazy('administration:coupons_list'),
        'form_title': f'Confirm Delete Coupon: {coupon_to_delete.code}',
        'user': request.user,
        'company': get_company_data()
    }
    # Reuse the generic confirm_delete template
    return render(request, 'administration/confirm_delete.html', context)


# View for Wishlists List
@login_required
@user_passes_test(is_staff_user)
def wishlists_list_view(request):
    """
    View to display a list of all wishlist items.
    Requires authentication and superuser status.
    """
    if not request.user.is_superuser:
        return redirect('administration:error_page')

    wishlists = Wishlist.objects.all().select_related('user', 'product') # Optimize query
    context = {
        'wishlists': wishlists,
        'user': request.user,
        'company': get_company_data()
    }
    return render(request, 'administration/wishlists_list.html', context)


# --- Settings Management Views ---

@login_required
@user_passes_test(lambda u: u.is_superuser) # Only superusers can edit company details
def company_details_view(request):
    """
    View to display and update the Company details.
    Assumes a single Company instance exists or handles creation if needed.
    """
    # Try to get the first Company instance, or create one if none exist
    company, created = Company.objects.get_or_create(
        pk=1, # Assuming pk=1 or use defaults if creating
        defaults={'name': 'Default Company Name'} # Provide sensible defaults
    )

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company details updated successfully!')
            # Redirect back to the same page to show updated details
            return redirect('administration:company_details')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CompanyForm(instance=company)

    context = {
        'form': form,
        'form_title': 'Update Company Details',
        'company_instance': company, # Pass the instance for display if needed
        'user': request.user,
        'company': company # Pass company data for base template context
    }
    return render(request, 'administration/company_form.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser) # Only superusers can edit delivery fee
def delivery_fee_view(request):
    """
    View to display and update the Delivery Fee.
    Assumes a single DeliveryFee instance exists or handles creation.
    """
    # Try to get the first DeliveryFee instance, or create one if none exist
    delivery_fee, created = DeliveryFee.objects.get_or_create(
        pk=1, # Assuming pk=1 or use defaults
        defaults={'fee': 0.0} # Default fee to 0
    )

    if request.method == 'POST':
        form = DeliveryFeeForm(request.POST, instance=delivery_fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delivery fee updated successfully!')
            # Redirect back to the same page
            return redirect('administration:delivery_fee')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DeliveryFeeForm(instance=delivery_fee)

    context = {
        'form': form,
        'form_title': 'Update Delivery Fee',
        'delivery_fee_instance': delivery_fee,
        'user': request.user,
        'company': get_company_data() # Pass company data for base template context
    }
    return render(request, 'administration/delivery_fee_form.html', context)