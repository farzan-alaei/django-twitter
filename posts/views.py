from django.shortcuts import render
from posts.forms import PostForm, ImageFormSet, CommentForm, ReactionForm
from posts.models import Post, Comment, Reaction
from django.views.generic import CreateView, ListView, DetailView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q


# Create your views here.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    message = 'Post created successfully'

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})

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
        messages.success(self.request, self.message)
        return super().form_valid(form)

    def save_images(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post = self.get_object()
        data['comment_form'] = CommentForm()
        data['reaction_form'] = ReactionForm()
        data['reactions'] = get_object_or_404(Post, pk=post.pk)
        data['comments'] = post.comments.all()
        return data


class AddCommentView(LoginRequiredMixin, FormView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/post_detail.html'

    def get_success_url(self):
        post_pk = self.kwargs.get('pk')
        return reverse_lazy('posts:post_detail', kwargs={'pk': post_pk})

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.user = self.request.user
        form.instance.post = post
        form.save()
        return super().form_valid(form)


class AddReactionView(LoginRequiredMixin, FormView):
    model = Reaction
    form_class = ReactionForm
    template_name = 'posts/post_detail.html'

    def get_success_url(self):
        post_pk = self.kwargs.get('pk')
        return reverse_lazy('posts:post_detail', kwargs={'pk': post_pk})

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        user = self.request.user
        if form.is_valid():
            liked = form.cleaned_data.get('liked')
            disliked = form.cleaned_data.get('disliked')

            existing_reaction = Reaction.objects.filter(
                Q(user=user) & Q(related_post=post)
            ).first()

            if existing_reaction:
                if liked and existing_reaction.liked:
                    existing_reaction.delete()
                elif disliked and existing_reaction.disliked:
                    existing_reaction.delete()
                else:
                    existing_reaction.liked = liked
                    existing_reaction.disliked = disliked
                    existing_reaction.save()
            else:
                form.instance.user = user
                form.instance.related_post = post
                form.save()

        return super().form_valid(form)
