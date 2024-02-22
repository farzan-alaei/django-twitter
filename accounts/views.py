from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import DetailView,View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,authenticate,logout
from django.core.exceptions import ValidationError
from django.views.generic import CreateView
from django.urls import reverse,reverse_lazy


from .models import User
from .forms import UserForm,RegisterForm
# Create your views here.

class Login(View):
    template_name="accounts/Login.html"
    form_class=UserForm
    def get(self,request):
        if request.user.is_authenticated:
            return HttpResponse('u are login now')
        else:
            form=self.form_class()
            return render(request,self.template_name,{'form':form})
        
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            # user=form.cleaned_data['user']
            # print(user)
            # login(request,user=user)
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(form)
            user = authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                print(user)                    
                login(request, user)
                # messages.success(request,f'Hi {username.title()}, welcome back!')
                # return redirect('posts')
            
                return HttpResponse("you login")
            elif user is None :
                return HttpResponse("user does not exist")
        else:
            print(form.is_valid)
            print(form.errors)
            return HttpResponse(":D")
    
class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
    def post(self,request):
        if request.user.is_authenticated:
            return redirect("login")
        else:
                form=RegisterForm(request.POST)
                if form.is_valid:
                    new_user=form.save(commit=False)
                    new_user.is_active=False
                    new_user.save()
                
                
                    return HttpResponse("you are register check email for verification")
                else:
                    raise ValidationError("check your fields again")
            
def emailconfirm(request):
    return render(request,'signed_up.html')