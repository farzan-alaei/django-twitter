from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import DetailView,View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,authenticate,logout
from django.core.exceptions import ValidationError

from .models import User
from .forms import UserForm
# Create your views here.

class Login(View):
    template_name="accounts/Login.html"
    form_class=UserForm
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        

        if form.is_valid():
            
            login(request,user=form.cleaned_data['user'])
            return HttpResponse('you login baby')
        
        else:
            raise ValidationError("your account is not active yet please check your email")


    
