from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UsernameField
from django.contrib.auth import authenticate
from .models import User
from django.conf import settings
from django.forms import EmailInput,TextInput,PasswordInput

class LoginForm(forms.Form):

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }))
    password = forms.CharField(required=True, widget=forms.PasswordInput({
        
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Password'
                }))
  
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is not None:
                cleaned_data['user'] = user
            else:
                raise forms.ValidationError("Invalid email or password.")

        return cleaned_data
        
class RegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "mobile",
                  "email",
                  'password1',
                  'password2',
                  )
        
    def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
            if password1 != password2:
                self.add_error('password2', forms.ValidationError('کلطه عبور با تکرارش تطابق ندارند', code='invalid'))
            cleaned_data.setdefault('password', password1)
            
            
            email = cleaned_data.get('email')
            user_registered= User.objects.filter(email=email)
            if user_registered.exists():
                self.add_error('email',forms.ValidationError('این ایمیل قبلا ثبت شده است',code='invali_email'))

            return cleaned_data  
    
    def save(self,commit=True):
            user=super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user

