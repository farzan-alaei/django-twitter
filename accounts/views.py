from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
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
from .models import User,UserFollowing
from .forms import LoginForm,RegisterForm
from django.utils.encoding import force_str
from django.contrib.auth.backends import ModelBackend
from chatapp.models import Room

from django.views.generic.edit import UpdateView


User = get_user_model()

class UserUpdateView(UpdateView):
    model = User
    fields = ['mobile','first_name','last_name']
    template_name_suffix = "update_form"

class LoginView(View):
    template_name='login.html'
    form_class = LoginForm
    
    def get(self,request):
        form=self.form_class
        return render(request,'accounts/login.html',{'form':form})
        
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            print('form is valid')
            user=form.cleaned_data.get('user')
            print(user.pk)
            login(request,user)
        else :
            return render(request,'accounts/login.html',{'form':form})
        return redirect('accounts:profile',pk=user.pk)
            

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("accounts:login")
        else:
            form=self.form_class
            return render(request,'accounts/signup.html',context={'form':form})
        
    def post(self,request):
        email_from = settings.EMAIL_HOST_USER
        subject="Welcome To Django Twitter"
        form=self.form_class(request.POST)
        print(form.errors)
        if form.is_valid:
            
            
                    new_user=form.save(commit=False)
                    new_user.is_active=False
                    new_user.save()
                    # template=get_template("acc_active_email.html")
                    token=account_activation_token.make_token(new_user)
                    uid = urlsafe_base64_encode(force_bytes(new_user.pk))
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
        else :
            return render(request,'accounts/signup.html',{'form':form},status=status)              
class active_user(View):
    def get (self,request,uidb64,token):
        try :
            uid = force_str(urlsafe_base64_decode(uidb64))
            user=get_user_model().objects.get(pk=uid)
            if user is not None and account_activation_token.check_token(user,token):
                user.is_active=True
                user.save()
                return render(request,'accounts/email_confirm.html')        
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user=None
            print('its nokey')  
            return HttpResponse('404')
        

class UserProfileDetailView(DetailView):
    model=User
    template_name="accounts/profile.html"
    context_object_name='profile'
    
    def get(self,request,pk):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        # if request.user.pk==int(pk):
        username = get_object_or_404(User, pk=int(pk))
        followers=UserFollowing.objects.filter(following_user_id=int(pk))
        following=UserFollowing.objects.filter(user_id=int(pk))
        related_user=UserFollowing.objects.select_related('user_id').all()
        # print(User.objects.select_related('following_user_id').all())
        # retrieved=User.objects.get(email=followers.following_user_id)
        # print(userretrieve)
        context ={
                'user':username,
                'request_user':request.user,
                'following':following,
                'followers':followers,
                'related':related_user
                # 'retrieved':retrieved
                
                
            }
        return render(request,template_name='accounts/profile.html',context=context)
        # else : 
        #     return HttpResponse('you are not allow to see here :)')
        
    def post (self,request,pk):
        follower=request.user
        following=User.objects.get(pk=pk)
        if UserFollowing.objects.filter(user_id=follower,following_user_id=following).exists():
            UserFollowing.objects.get(user_id=follower,following_user_id=following).delete()
            return render(request,'accounts/profile.html')

        else :
            new=UserFollowing.objects.create(user_id=follower,following_user_id=following)
            new.save()
            context={
                'new':new
            }
            
            return render(request,'accounts/profile.html',context)

def unfollow_user(request,pk):
    if request.method=='POST':
        follower=request.user
        following=User.objects.get(pk=pk)
        new=UserFollowing.objects.create(user_id=follower,following_user_id=following)
        new.save()
