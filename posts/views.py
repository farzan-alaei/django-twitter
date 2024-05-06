from django.shortcuts import render
from posts.forms import PostForm, ImageFormSet, CommentForm, ReactionForm
from posts.models import Post, Comment, Reaction
from django.views.generic import CreateView, ListView, DetailView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404


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

    def get_queryset(self):
        return Post.objects.filter(archived=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['object_list']
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post = self.get_object()
        likes, dislikes = post.count_reactions()
        if post.archived:
            raise Http404("Post does not exist")
        data['comment_form'] = CommentForm()
        data['reaction_form'] = ReactionForm()
        data['reactions'] = get_object_or_404(Post, pk=post.pk)
        data['comments'] = post.comments.all()
        data['tags'] = post.tags.all()
        data['likes'] = likes
        data['dislikes'] = dislikes
        return data


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'

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
        return super().form_valid(form)

    def save_images(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()


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
    """
    A class-based view that handles adding reactions (likes/dislikes) to posts.
    Requires users to be logged in.
    """

    model = Reaction
    form_class = ReactionForm
    template_name = 'posts/post_detail.html'

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.
        """
        post_pk = self.kwargs.get('pk')
        return reverse_lazy('posts:post_detail', kwargs={'pk': post_pk})

    def form_valid(self, form):
        """
        Handles valid form submissions and updates or creates user reactions.
        Args:
            form (Form): The validated reaction form.
        Returns:
            HttpResponseRedirect: The response object with the redirect URL.
        """

        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        user = self.request.user
        liked = self.request.POST.get('liked', False)
        disliked = self.request.POST.get('disliked', False)

        reaction, created = Reaction.objects.update_or_create(
            user=user, related_post=post, defaults={'liked': liked, 'disliked': disliked}
        )

        if not created and (liked == reaction.liked and disliked == reaction.disliked):
            reaction.delete()  # Remove unchanged reaction

        return super().form_valid(form)
