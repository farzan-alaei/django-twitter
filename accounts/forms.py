from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UsernameField
from django.contrib.auth import authenticate
from .models import User

class UserForm(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data=super().clean()
        username=cleaned_data['email']
        password=cleaned_data['password']
        user=authenticate(username=username,password=password)
        
        if user is not None:
             cleaned_data['user']=user
             return cleaned_data
        if user is None:
                raise forms.ValidationError("User does not exist.")
        
class RegisterForm(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("first_name","last_name",
                  "mobile",
                  "email",
                  "password")
        def clean(self):
            cleaned_data=super().clean()
            password=cleaned_data.get("password")
            confirm_password=cleaned_data.get("confirm_password")
            if password != confirm_password :
                raise forms.ValidationError("password and confirmed password does not match")
