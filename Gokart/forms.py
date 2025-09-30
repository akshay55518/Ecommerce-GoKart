from django import forms
from django.contrib.auth.forms import UserCreationForm ,PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control','id':'floatingInput'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','id':'floatingInput'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','address','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={
                                'placeholder':'Enter your Old Password',
                                'class':'form-control',
                                'autofocus':'True',
                                'autocomplete':'current-password'}))
    new_password1=forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
                                'placeholder':'Enter your Old Password',
                                'class':'form-control',
                                'autocomplete':'current-password'}))
    new_password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
                                'placeholder':'Enter your Old Password',
                                'class':'form-control',
                                'autocomplete':'current-password'}))
    
class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}))