from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

from userauths.models import User , Profile , Address , Phone , CreditCard

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'First Name'}), max_length=100, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Last Name'}), max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Username'}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;' , 'id': "", 'placeholder':'Email Address'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1' , 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'with-border'




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;',
            'placeholder': 'Old Password'
        }),
        required=True
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;',
            'placeholder': 'New Password'
        }),
        required=True
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;',
            'placeholder': 'Confirm New Password'
        }),
        required=True
    )



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )


    class Meta:
        model = Profile
        fields = ['cover_images']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            profile.save()

        return profile

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Last Name'
        })
    )
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    
    # Boolean field for verification status
    verified = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    # Select fields for existing addresses and phones
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),  # Will be set in __init__
        required=False,
        empty_label="-- Select Address --",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'disabled': 'true'
        })
    )
    
    phone = forms.ModelChoiceField(
        queryset=Phone.objects.none(),  # Will be set in __init__
        required=False,
        empty_label="-- Select Phone --",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'disabled': 'true'
        })
    )

    class Meta:
        model = Profile
        fields = ['cover_images', 'verified']
        widgets = {
            'cover_images': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; padding: 10px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Set initial user data
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['username'].initial = user.username
            
            # Set querysets for address and phone selection
            self.fields['address'].queryset = Address.objects.filter(user=user)
            self.fields['phone'].queryset = Phone.objects.filter(user=user)
            
            # If user has profile, set cover image and verified status
            if hasattr(user, 'profile'):
                self.instance = user.profile
                self.fields['verified'].initial = user.profile.verified

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if username exists but is not the current user's username
        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        
        # Update user info
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        
        # Update profile verified status
        profile.verified = self.cleaned_data['verified']

        if commit:
            user.save()
            profile.save()

        return profile

class PhoneUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Phone
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must be numeric.")
        return phone





class AddressUpdateForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
        required=True
    )

    class Meta:
        model = Address
        fields = ['type', 'address', 'notes']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional notes', 'rows': 2}),
        }





class CreditCardForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cardholder Name'}),
        required=True
    )
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
        required=True
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=True
    )
    cvv = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV', 'maxlength': '3'}),
        required=True
    )
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )

    class Meta:
        model = CreditCard
        fields = ['name', 'card_number', 'country', 'cvv', 'expiration_date']




User = get_user_model()

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email.")
        return email




class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
