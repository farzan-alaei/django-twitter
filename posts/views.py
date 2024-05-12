from django.shortcuts import render, redirect
from posts.forms import PostForm, ImageFormSet, CommentForm, ReactionForm
from posts.models import Post, Comment, Reaction
from django.views.generic import CreateView, ListView, DetailView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
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
        """
        Retrieves the context data for the view.
        Args:
            **kwargs: Additional keyword arguments.
        Returns:
            dict: The context data for the view.
        This method overrides the `get_context_data` method of the parent class.
        It retrieves the context data by calling the parent class method with the provided keyword arguments.
        It sets the 'image_formset' key in the context data by creating an instance of `ImageFormSet` with the request
        POST data and request files, or with the instance of the current object if the request POST data is empty.
        The resulting context data is returned.
        """

        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['image_formset'] = ImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """
        Validates the form and saves the associated post.
        Sets the user of the form instance to the current request user.
        Saves the form and the associated object, saves any images related to the post,
        adds a success message, and invokes the parent class's form_valid method with the form.
        Returns the result of the parent class's form_valid method.
        """

        form.instance.user = self.request.user
        self.object = form.save()
        self.save_images(form)
        messages.success(self.request, self.message)
        return super().form_valid(form)

    def save_images(self, form):
        """
        Saves the images associated with the post.
        Parameters:
            form (Form): The form containing the post data.
        Returns:
            None
        """

        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(archived=False).order_by('-created_at').prefetch_related('comments')

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view.
        Args:
            **kwargs: Additional keyword arguments.
        Returns:
            dict: The context data for the view.
        This method overrides the `get_context_data` method of the parent class.
        It retrieves the context data by calling the parent class method with the provided keyword arguments.
        It sets the 'reaction_form' key in the context data by creating an instance of `ReactionForm`.
        The resulting context data is returned.
        """

        context = super().get_context_data(**kwargs)
        context['reaction_form'] = ReactionForm()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view.
        Args:
            **kwargs: Additional keyword arguments.
        Returns:
            dict: The context data for the view.
        This method overrides the `get_context_data` method of the parent class.
        It retrieves the context data by calling the parent class method with the provided keyword arguments.
        It sets the 'comment_form', 'reaction_form', 'reactions', 'comments',
        'tags', 'likes', and 'dislikes' keys in the context data.
        """

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

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches the request to the appropriate handler method.
        Parameters:
            request: The request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.
        Returns:
            The result of the dispatch method.
        """

        self.object = self.get_object()
        if self.object.user != self.request.user:
            raise Http404("You are not allowed to update this post.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for the view based on the provided keyword arguments.
        Sets 'image_formset' in the context data based on the request POST data and files.
        Returns the updated context data.
        """

        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['image_formset'] = ImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """
        Validates the form and saves the associated post.

        Args:
            form (Form): The form containing the post data.

        Returns:
            HttpResponse: The response object with the redirect URL.

        This method sets the user of the form instance to the current request user,
        saves the form and the associated object, saves any images related to the post,
        and invokes the parent class's form_valid method with the form.
        The result of the parent class's form_valid method is returned.
        """

        form.instance.user = self.request.user
        self.object = form.save()
        self.save_images(form)
        return super().form_valid(form)

    def save_images(self, form):
        """
        Save the images associated with the post.
        Parameters:
            form (Form): The form containing the post data.
        Returns:
            None
        This method retrieves the image formset from the context data and checks if it is valid.
        If it is valid, it sets the instance of the image formset to the current object and saves it.

        """
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
        next_page = self.request.GET.get('next', None)
        if next_page == 'list':
            return reverse_lazy('posts:post_list')
        else:
            post_pk = self.kwargs.get('pk')
            return reverse_lazy('posts:post_detail', kwargs={'pk': post_pk})

    def form_valid(self, form):
        """
        Validates the form and saves the associated comment.
        Args:
            form (CommentForm): The form containing the comment data.
        Returns:
            HttpResponse: The response object with the redirect URL.
        Raises:
            Http404: If the post with the given primary key does not exist.
        """
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.user = self.request.user
        form.instance.post = post
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data by calling the parent class method with the provided keyword arguments.
        Sets 'reply_to_form' in the context by invoking 'get_reply_to_form'.
        Returns the updated context.
        """
        context = super().get_context_data(**kwargs)
        context['reply_to_form'] = self.get_reply_to_form()
        return context

    def post(self, request, *args, **kwargs):
        """
            Handles the POST request. Processes the reply form data if present.
            Redirects to the success URL if the reply form is valid.
            Raises an exception if the reply form is not valid.
        """
        if 'reply_to_comment_id' in request.POST:
            reply_to_form = self.get_reply_to_form(request.POST)
            if reply_to_form.is_valid():
                post_pk = self.kwargs.get('pk')
                post = get_object_or_404(Post, pk=post_pk)
                reply_to_form.instance.user = self.request.user
                reply_to_form.instance.post = post
                reply_to_form.save()
                return redirect(self.get_success_url())
            else:
                raise Exception('Reply form is not valid.')

        return super().post(request, *args, **kwargs)

    def get_reply_to_form(self, data=None):
        """
        Generates a reply form for the given data.
        Parameters:
            data (dict, optional): The data to initialize the form with. Defaults to None.
        Returns:
            CommentForm: The reply form without the 'reply_to' field.
        """
        reply_to_form = CommentForm(data)
        del reply_to_form.fields['reply_to']
        return reply_to_form


class AddReactionView(LoginRequiredMixin, FormView):
    """
    A class-based view that handles adding reactions (likes/dislikes) to posts.
    Requires users to be logged in.
    """

    model = Reaction
    form_class = ReactionForm
    template_name = ['posts/post_detail.html', 'posts/post_list.html']

    def get_success_url(self):
        next_page = self.request.GET.get('next', None)
        if next_page == 'list':
            return reverse_lazy('posts:post_list')
        else:
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

        try:
            reaction = Reaction.objects.get(user=user, related_post=post)
        except Reaction.DoesNotExist:
            reaction = None

            # Handle reaction based on existing reaction and new values
        if reaction:
            if liked == str(reaction.liked) and disliked == str(reaction.disliked):
                # Delete unchanged reaction
                reaction.delete()
            else:
                # Update reaction with new values
                reaction.liked = liked
                reaction.disliked = disliked
                reaction.save()
        else:
            # Create new reaction
            reaction = Reaction.objects.create(
                user=user, related_post=post, liked=liked, disliked=disliked
            )

        return super().form_valid(form)
