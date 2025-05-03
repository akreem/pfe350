from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator # Import RegexValidator
from products.models import Brand ,Product, ProductImage
from userauths.models import Address, Phone, CreditCard # Import Address, Phone and CreditCard models
from orders.models import Order,Coupon # Import Order model
import datetime

class BrandForm(forms.ModelForm):
    """
    Form for creating and updating Brand objects.
    """
    class Meta:
        model = Brand
        fields = ['name', 'image']
        labels = {
            'name': _('Brand Name'),
            'image': _('Brand Logo/Image'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'name': _('Enter the name of the brand.'),
            'image': _('Upload an image representing the brand (e.g., logo).'),
        }
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserCreationForm(UserCreationForm):
    """
    A form for creating new users by an administrator.
    Includes fields for basic user info and status flags.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ( 'first_name', 'last_name', 'username', 'email', 'is_staff', 'is_superuser') # Add relevant fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent styling if needed
        for field_name, field in self.fields.items():
            if field_name in ['is_staff', 'is_active', 'is_superuser']:
                # Apply form-check-input class specifically to boolean fields
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Apply standard form-control class to other fields
                field.widget.attrs['class'] = 'form-control mb-2'


class AdminUserChangeForm(UserChangeForm):
    """
    A form for updating existing users by an administrator.
    Password field is removed as password changes should be handled separately.
    """
    password = None # Remove password field from admin change form

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent styling if needed
        for field_name, field in self.fields.items():
            # Avoid styling non-editable fields if any are added later
            if field_name not in getattr(self.Meta, 'read_only_fields', []):
                if field_name in ['is_staff', 'is_active', 'is_superuser']:
                     # Apply form-check-input class specifically to boolean fields
                    field.widget.attrs['class'] = 'form-check-input'
                else:
                    # Apply standard form-control class to other fields
                    field.widget.attrs['class'] = 'form-control mb-2'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        # Ensure result is always a list, even if one file is uploaded
        return result if isinstance(result, list) else [result] if result else []


class ProductForm(forms.ModelForm):
    # Add the field for multiple image uploads
    # 'required=False' because images might already exist (on update)
    # or user might not upload any new ones.
    # Use 'new_images' to avoid clashing with the model's 'image' field.
    new_images = MultipleFileField(label='Add/Replace Images', required=False)

    class Meta:
        model = Product
        # Keep 'image' as the primary display image.
        fields = ['name', 'flag', 'image', 'price', 'sku', 'subtitle', 'descripition', 'quantity', 'brand', 'tags']
        widgets = {
            'descripition': forms.Textarea(attrs={'rows': 4}),
            # 'tags' widget might need specific configuration depending on the library used (e.g., select2)
            # We'll apply base styling in __init__
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent Bootstrap 5 styling
        for field_name, field in self.fields.items():
            widget = field.widget
            current_attrs = widget.attrs
            new_class = ''

            # Determine the correct Bootstrap class based on widget type
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.PasswordInput, forms.URLInput, forms.Textarea, forms.ClearableFileInput, MultipleFileInput)):
                new_class = 'form-control mb-2'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                new_class = 'form-select mb-2'
            elif isinstance(widget, forms.CheckboxInput):
                new_class = 'form-check-input' # Checkboxes usually don't need mb-2 directly on input
            elif isinstance(widget, forms.RadioSelect):
                # Radio buttons often require styling on the label or wrapper
                pass # No default class added directly to the widget container

            # Apply the new class, preserving existing attributes like 'rows'
            if new_class:
                updated_attrs = current_attrs.copy()
                updated_attrs['class'] = new_class
                widget.attrs = updated_attrs

            # Special handling for description rows attribute if not already handled
            if field_name == 'descripition' and 'rows' not in widget.attrs:
                 widget.attrs['rows'] = 4 # Ensure rows attribute is present

            # Ensure the custom MultipleFileInput gets the class too
            if field_name == 'new_images' and isinstance(widget, MultipleFileInput):
                 widget.attrs['class'] = 'form-control mb-2'
class AddressForm(forms.ModelForm):
    """
    Form for creating Address objects.
    """
    class Meta:
        model = Address
        fields = ['user', 'type', 'address', 'notes'] # Corrected fields
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}), # Changed from address_type
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), # Changed from street_address, city etc. to single address field
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class PhoneForm(forms.ModelForm):
    """
    Form for creating Phone objects.
    """
    class Meta:
        model = Phone
        fields = ['user', 'type', 'phone'] # Corrected fields (removed is_default)
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
class CreditCardForm(forms.ModelForm):
    """
    Form for creating CreditCard objects.
    """
    # Add validation for card number: exactly 16 digits
    card_number = forms.CharField(
        label=_('Card Number'),
        max_length=16,
        min_length=16,
        validators=[RegexValidator(r'^\d{16}$', 'Enter a valid 16-digit card number.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16', 'placeholder': 'XXXXXXXXXXXXXXXX'})
    )

    # Use DateInput for better UX for expiration_date
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_('Expiration Date')
    )

    # Add validation for CVV: exactly 3 digits
    cvv = forms.CharField(
        label=_('CVV'),
        max_length=3,
        min_length=3,
        validators=[RegexValidator(r'^\d{3}$', 'Enter a valid 3-digit CVV.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3', 'placeholder': 'XXX'})
    )

    class Meta:
        model = CreditCard
        fields = ['user', 'name', 'card_number', 'country', 'cvv', 'expiration_date', 'image']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'card_number' widget is defined in the field declaration above
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            # 'cvv' widget is defined in the field declaration above
            # 'expiration_date' widget is defined above
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Name on Card'),
            'cvv': _('CVV'),
            'image': _('Card Image (Optional)'),
        }
        help_texts = {
            'card_number': _('Enter the 16-digit card number.'),
            'cvv': _('Enter the 3-digit security code.'),
        }


class OrderForm(forms.ModelForm):
    """
    Form for updating Order objects, specifically the status.
    """
    class Meta:
        model = Order
        fields = ['status'] # Only allow updating the status
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select mb-2'}),
        }
        labels = {
            'status': _('Order Status'),
        }
        help_texts = {
            'status': _('Select the current status of the order.'),
        }


class OrderCreateForm(forms.ModelForm):
    """
    Form for creating new Order objects (basic details).
    """
    class Meta:
        model = Order
        # Include fields necessary for creation.
        # Exclude fields that should be calculated or set automatically (like total_price, code, order_time).
        fields = ['user', 'status', 'coupon'] # Add 'coupon' if applicable and desired during creation
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select mb-2'}),
            'status': forms.Select(attrs={'class': 'form-select mb-2'}),
            'coupon': forms.Select(attrs={'class': 'form-select mb-2'}), # Assuming coupon is a ForeignKey
        }
        labels = {
            'user': _('Customer'),
            'status': _('Initial Order Status'),
            'coupon': _('Apply Coupon (Optional)'),
        }
        help_texts = {
            'user': _('Select the user placing the order.'),
            'status': _('Set the initial status for this order.'),
            'coupon': _('Select a coupon to apply to this order, if any.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the user field required for creation
        if 'user' in self.fields:
            self.fields['user'].required = True
            self.fields['user'].help_text = _('Select the user placing the order. This field is required.') # Update help text

        # Make coupon optional if it's allowed to be blank/null in the model
        if 'coupon' in self.fields:
            self.fields['coupon'].required = False
from django.forms import inlineformset_factory
from orders.models import Order, OrderDetails # Import OrderDetails

class OrderDetailForm(forms.ModelForm):
    """
    Form for individual OrderDetail items within the inline formset.
    """
    class Meta:
        model = OrderDetails
        # Include fields relevant for admin editing
        # 'price' can be included, but the model's save method handles it if empty.
        # 'total' is calculated automatically.
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select form-select-sm'}), # Use smaller select for inline
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': '1'}), # Use smaller input
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}), # Use smaller input
        }
        labels = {
            'product': _('Product'),
            'quantity': _('Qty'),
            'price': _('Price (Override)'), # Label indicates it overrides product price
        }
        help_texts = {
            'price': _('Leave blank to use the current product price.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make price not required and always disabled
        self.fields['price'].required = False
        self.fields['price'].disabled = True # Disable price field always
        self.fields['price'].help_text = _('Price is set automatically based on the selected product (read-only).') # Consistent help text

        # Check if this form instance is for an existing OrderDetail (i.e., being updated)
        if self.instance and self.instance.pk:
            # If updating, also disable product and quantity fields
            self.fields['product'].disabled = True
            self.fields['quantity'].disabled = True
            # Price is already disabled above
        # else: product and quantity remain enabled for creation


# Create an inline formset for OrderDetails linked to Order
# Default settings allow adding/deleting for the CREATE view.
# We will override these in the UPDATE view.
# Formset for CREATING orders: allows adding 3 extra items and deleting
OrderDetailCreateInlineFormSet = inlineformset_factory(
    Order,
    OrderDetails,
    form=OrderDetailForm,
    extra=3, # Show 3 blank forms by default for adding items
    can_delete=True, # Allow deleting items by default (for create view)
    fk_name='order' # Specify the foreign key field name
)


class CouponForm(forms.ModelForm):
    """
    Form for creating and updating Coupon objects.
    """
    # Use DateInput for better UX for date fields
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_('Start Date'),
        initial=datetime.date.today # Default to today
    )
    

    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'quantity', 'start_date', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            # 'start_date' and 'end_date' widgets defined above
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'code': _('Coupon Code'),
            'discount': _('Discount Percentage'),
            'quantity': _('Available Quantity'),
            'image': _('Coupon Image (Optional)'),
        }
        help_texts = {
            'code': _('Enter a unique code for the coupon.'),
            'discount': _('Enter the discount percentage (0-100).'),
            'quantity': _('How many times can this coupon be used?'),
            
        }

# Formset for UPDATING orders: prevents adding extra items or deleting existing ones via formset
OrderDetailUpdateInlineFormSet = inlineformset_factory(
    Order,
    OrderDetails,
    form=OrderDetailForm,
    extra=0, # Do not show extra blank forms
    can_delete=False, # Do not allow deleting items via the formset in update view
    fk_name='order' # Specify the foreign key field name
)