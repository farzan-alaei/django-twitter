from django.contrib import admin
from django.urls import path,include
from .views import RegisterView,active_user,LoginView,UserProfileDetailView,UserUpdateView
from django.conf.urls.static import static  
from django.conf import settings

app_name='accounts'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('activate/<uidb64>/<token>',active_user.as_view(),name='activate'),
    path('profile/<int:pk>',UserProfileDetailView.as_view(),name='profile'),
    path('update/<pk>',UserUpdateView.as_view(),name='update'),

    # path('profile/<int:pk>',follow_user,name='follow')

    # path('profile/',user_info,name='profile')

]
