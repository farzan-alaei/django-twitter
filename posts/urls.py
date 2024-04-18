from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
