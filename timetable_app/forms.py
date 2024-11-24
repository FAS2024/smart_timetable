# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import IdentificationNumber
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm




class VerifyIdentificationNumberForm(forms.Form):
    identification_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Identification Number'}),
        label='Identification Number'
    )
    
    
class UserRegistrationForm(UserCreationForm):
    """
    Custom registration form that includes the identification number (read-only),
    email, password, and other fields.
    """
    identification_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Identification Number'
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        label='Email'
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        label='Phone Number'
    )

    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}),
        label='Address'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ['identification_number', 'email', 'phone', 'address', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("The two password fields must match.")

        return cleaned_data

        
    

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone = forms.CharField(required=True, max_length=20)
#     address = forms.CharField(required=True, max_length=150)

#     class Meta:
#         model = CustomUser
#         fields = ['identification_number', 'email', 'phone', 'address', 'password1', 'password2']

#     def clean_identification_number(self):
#         identification_number = self.cleaned_data.get('identification_number')
#         if CustomUser.objects.filter(identification_number=identification_number).exists():
#             raise forms.ValidationError("A user with this identification number already exists.")
#         return identification_number



class IdentificationNumberForm(forms.ModelForm):
    class Meta:
        model = IdentificationNumber
        fields = ['number', 'role']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Identification Number'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'number': 'Identification Number',
            'role': 'Role',
        }

