from django.contrib import admin
from django.urls import path
from .views import Login
app_name='accounts'
urlpatterns = [
    # path('profile/<int:pk>',UserProfile.as_view(),name='profile'),

    path('login', Login.as_view(),name='login')

    
]
