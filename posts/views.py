from django.shortcuts import render
from posts.forms import PostForm, ImageFormSet
from posts.models import Post
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy


# Create your views here.


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:post_create')
    message = 'Post created successfully'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['image_formset'] = ImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.save_images(form)
        return super().form_valid(form)

    def save_images(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'