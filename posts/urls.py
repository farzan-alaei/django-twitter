from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('add_comment/<int:pk>/', views.AddCommentView.as_view(), name='add_comment'),
    path('add_reaction/<int:pk>/', views.AddReactionView.as_view(), name='add_reaction'),
]
