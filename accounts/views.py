from email.message import EmailMessage
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import DetailView,View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.core.exceptions import ValidationError
from django.core import mail
from django.views.generic import CreateView
from django.urls import reverse,reverse_lazy
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.html import strip_tags
from base64 import urlsafe_b64encode
from .tokens import account_activation_token
from django.conf import settings
from .models import User
from .forms import UserForm,RegisterForm
# Create your views here.

user=get_user_model()

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
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("accounts:login")
        else:
            form=RegisterForm
            return render(request,'accounts/signup.html',context={'form':form})
        
    def post(self,request):
        email_from = settings.EMAIL_HOST_USER
        subject="Welcome To Django Twitter"
        form=RegisterForm(request.POST)
        if form.is_valid:
                    new_user=form.save(commit=False)
                    new_user.is_active=False
                    new_user.save()
                    # template=get_template("acc_active_email.html")
                    token=account_activation_token.make_token(new_user)    
                    uid = urlsafe_b64encode(force_bytes(user.pk))   
                    current_site = get_current_site(request)
                    context={
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid':uid,
                    'token':token,}
                    html_message = render_to_string('accounts/acc_active_email.html', context)     
                    plain_message = strip_tags(html_message)
                    # email= EmailMessage(subject,html_message,email_from,[new_user.email])
                    mail.send_mail(subject,plain_message,email_from,[new_user.email],html_message=html_message)
                    status=200
                    return HttpResponse('check your email for verification check spam folder too')
        else:
                    messages.error(request, 'Error')
                    status = 400
                    return HttpResponse("ur register has an error")
                
def emailconfirm(request):
    return render(request,'signed_up.html')