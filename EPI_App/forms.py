from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, ProductScheme, pay_his

class SignupForm(forms.ModelForm):
    accept_terms = forms.BooleanField(
        required=True, 
        label="I accept the Terms and Conditions.",
        error_messages={'required': "You must accept the terms and conditions to register."},
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter username', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'}),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'}),
    )

    kyc_document = forms.FileField(
        required=True,
        label="Upload KYC Document",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    kyc_document_type = forms.ChoiceField(
        required=True,
        label="Document Type",
        choices=[
            ('passport', 'Passport'),
            ('aadhaar', 'Aadhaar Card'),
            ('license', 'Driver’s License'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    pan_card = forms.FileField(
        required=True,
        label="Upload PAN Card",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    bank_passbook = forms.FileField(
        required=True,
        label="Upload Bank Passbook",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match.")
        return password2
    
    def clean_kyc_document(self):
        document = self.cleaned_data.get('kyc_document')
        if document.size > 5 * 1024 * 1024:  # Limit size to 5MB
            raise ValidationError("Document size cannot exceed 5MB.")
        if not document.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):  # Restrict file types
            raise ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        if not document:
            raise ValidationError("KYC document is required.")
        return document

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['kyc_document_type', 'kyc_document', 'pan_card', 'bank_passbook']

class ProductSchemeForm(forms.ModelForm):
    class Meta:
        model = ProductScheme
        fields = ['product_id','investment', 'total', 'days']



class PayHisForm(forms.ModelForm):
    class Meta:
        model = pay_his
        fields = ['product_id', 'title', 'investments', 'total', 'balance', 'backcount']