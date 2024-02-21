from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

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
        else:
            raise forms.ValidationError("Credentional is invalid")
        
    