from django import forms
from .models import Post, Image, Comment, Reaction
from django.forms import inlineformset_factory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'reply_to']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags']


class ReactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['liked'] = instance.liked
            self.initial['disliked'] = instance.disliked

    class Meta:
        model = Reaction
        fields = ['liked', 'disliked']


ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=1, can_delete=True)
